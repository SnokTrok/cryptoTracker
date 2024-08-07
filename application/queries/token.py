import sqlalchemy
from typing import Tuple
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import or_
import pandas as pd
import numpy as np

from cryptoTracker.db.utils import get_pg_db
from cryptoTracker.orm.crypto.tokens import (
    Token , TokenPriceHistory
)


# region ---- UPSERT -----------------------------

def upsert_token(df_token : pd.DataFrame):
    """
        Upsert Token info to crypto.token
    """
    with get_pg_db().session_scope() as session:
          # replacing pd.NA with NONE for sqlalchemy to format qry correctly...
        
        data_to_upsert = df_token.rename({'token_name' : 'name'},axis=1).astype(object).where(pd.notnull, None).to_dict(orient='records')
        upsert_stmt = insert(Token).values(data_to_upsert)
        upsert_stmt = upsert_stmt.on_conflict_do_update(
            index_elements=['identifier'],
            set_=dict(
                name=upsert_stmt.excluded.name,
                chain=upsert_stmt.excluded.chain,
                eth_contract_address=upsert_stmt.excluded.eth_contract_address
            )
        )
        session.execute(upsert_stmt)
        

def validate_token_info(token_identifier : str = None, token_id : int = None) -> bool:
    """
        check if we have current token data for supplied fields...
    """
    if token_identifier == None and token_id == None:
        raise ValueError('args must contain one of either token_name OR token_id')
    
    with get_pg_db().session_scope() as session:
        try:
            if token_id is not None:
                qry = (session.query(Token).where(Token.id==int(token_id)).one())
                return True
            qry = (session.query(Token).where(Token.identifier==token_identifier).one())
            return True
        except Exception as e:
            print(e)
            print(f"Could not find token with token_identifier : {token_identifier} or token_id : {token_id}")
            return False
        


def upsert_token_price_history(df_history : pd.DataFrame,token_id = None):
    """
        Update existing data with df_history , insert new data...
    """
    with get_pg_db().session_scope() as session:

        # first check our token exists , using .one() will throw error is None or multiple found.
       
        if  validate_token_info(token_id=token_id) == False:
            raise ValueError('failed to validate token_id')
        
        # replacing pd.NA with NONE for sqlalchemy to format qry correctly , None -> NULL pd.NA will throw error

        df_history['token_id'] = token_id

        print(f"Upserting {len(df_history)} records into price_history for token {token_id}")
        data_to_upsert = df_history.astype(object).where(pd.notnull, None).to_dict(orient='records')
        upsert_stmt = insert(TokenPriceHistory).values(data_to_upsert)
        upsert_stmt = upsert_stmt.on_conflict_do_update(
            index_elements=['token_id','date_open'],
            set_=dict(
                date_close=upsert_stmt.excluded.date_close,
                price_open=upsert_stmt.excluded.price_open,
                price_close=upsert_stmt.excluded.price_close,
                price_high=upsert_stmt.excluded.price_high,
                price_low=upsert_stmt.excluded.price_low,
                volume=upsert_stmt.excluded.volume,
                num_trades=upsert_stmt.excluded.num_trades
            )
        )
        session.execute(upsert_stmt)


def get_tokens() -> Tuple[pd.DataFrame,list[Token]]:
    """
        Pull entire token table , returning both df and token objects
    """
    with get_pg_db().session_scope() as  session:
        qry = (
            session.query(Token)
        )
        type_map = {
            'id' : 'Int64',
            'name' : 'string',
            'identifier' : 'string',
            'chain' : 'string',
            'eth_contract_address' : 'string'
        }
        df = pd.read_sql_query(qry.statement,session.bind,dtype=type_map)
        return df , qry.all()


def get_price_history(token_id : int) -> pd.DataFrame:
    """
        Get historical price of token filtered by token_id

        likely we are going to want to get the tokens via ORM token.price_history, BUT this is here in case we need it
    """
    type_map = {
        'price_high': 'Float64',
        'price_low' : 'Float64',
        'price_open': 'Float64',
        'price_close' : 'Float64',  
        'volume' : 'Float64',
        'num_trades' : 'Int64'
    }
    date_cols = ['date_open', 'date_close']
    if validate_token_info(token_id=token_id) :
        with get_pg_db().session_scope() as session:
            qry = session.query(TokenPriceHistory).where(TokenPriceHistory.token_id==int(token_id))
            df = pd.read_sql_query(qry.statement,session.bind,dtype=type_map,parse_dates=date_cols)
            return df
        

# endregion. -----------------------------------------


