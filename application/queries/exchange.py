import sqlalchemy
from typing import Tuple
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import or_
import pandas as pd
import numpy as np
from pandera import check_input , check_output
from cryptoTracker.db.utils import get_pg_db
from cryptoTracker.orm.crypto.exchange import (
    TokenExchangePriceHistory,
    ExchangeToken
)

def get_exhange_tokens(token_id : int = None) -> pd.DataFrame:
    """
        get all  exchage tokens ...
    """
    with get_pg_db().session_scope() as  session:
        qry = (session.query(ExchangeToken))
        type_map = {
            'id' : 'Int64',
            'name' : 'string'
        }
        df = pd.read_sql_query(qry.statement,session.bind,dtype=type_map)

        return df
    
    
def validate_exchange_token(token_name : str = None , token_id : int = None) -> bool:
    if token_name == None and token_id == None:
        raise ValueError('args must contain one of either token_name OR token_id')
    
    with get_pg_db().session_scope() as session:
        try:
            if token_id is not None:
                qry = (session.query(ExchangeToken).where(ExchangeToken.id==int(token_id)).one())
                return True
            qry = (session.query(Token).where(Token.name==token_name).one())
            return True
        except Exception as e:
            print(e)
            print(f"Could not find token with token_name : {token_name} or token_id : {token_id}")
            return False


def get_price_history(token_id : int):
    """

    """
    with get_pg_db().session_scope() as  session:
        qry = (session.query(ExchangeToken))

        if(token_id != None) and validate_exchange_token({'token_id' : token_id}):
            qry = qry.filter(ExchangeToken.id == token_id)
        
        parse_dates = ['date_open' , 'date_close']
        type_map = {
            'token_id' : 'Int64',
            'price_open' : 'Float64',
            'price_close' : 'Float64',
            'price_high' : 'Float64',
            'price_low' : 'Float64'
        }
        df = pd.read_sql_query(qry.statement,session.bind,dtype=type_map,parse_dates=parse_dates)

        return df
        

def insert_missing_tokens(tokens : list[str]):
    with get_pg_db().session_scope() as session:
        insert_qry = insert(ExchangeToken).values({"name" : t for t in tokens})
        print("Inserting missing exchange tokens...")
        session.execute(insert_qry)