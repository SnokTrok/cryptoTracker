import pandas as pd
from pandera import check_output
from cryptoTracker.application.utils import get_secret
from cryptoTracker.application.queries.token import (
    upsert_token , upsert_token_price_history, validate_token_info,
    get_tokens
)
from cryptoTracker.application.OHLCscan.models.api import OHLCPricesRequest
from cryptoTracker.application.OHLCscan.api import get_OHLC_price_history

class CoinPriceExtractor():

    def __init__(self) -> None:
         self.token_info = get_secret('token')
       

    def get_tokens_from_secrets(self) -> pd.DataFrame:
        """
            Optional to retrive from secrets, for repulling historical data use from_postgres.
        """
        self.token_info = get_secret('token')

        token_data = {
            'name' : [],
            'identifier' : [],
            'eth_contract_address' :  [],
            'chain' : []
        }
        for token , token_info in self.token_info.items():
            identifier = token_info['identifier']

            if not validate_token_info(token_identifier=identifier):
                token_data['name'].append(token_info['name'])
                token_data['identifier'].append(token_info['identifier'])
                token_data['chain'].append(token_info['chain'])
                try:
                    token_data['eth_contract_address'].append(token_info['eth_contract_address'])
                except:
                    token_data['eth_contract_address'].append(pd.NA)


        # TODO : move over to pandera for df schema validation...
        token_data = pd.DataFrame(token_data).astype({'name' : 'string' , 'identifier' : 'string', 'chain' : 'string' , 'eth_contract_address' : 'string'})
        if not token_data.empty:
            print(f"Upserting {len(token_data)} new tokens.")
            upsert_token(token_data)

        return token_data


    def extract_history(self,date_start  : str, date_end : str, from_secrets : bool = False) -> pd.DataFrame:
        """
            Go through each token extracting history , inject token specific info,
        """

        if from_secrets:
            df_tokens = self.get_tokens_from_secrets()

        df_tokens , _ = get_tokens()

        for token in df_tokens.itertuples():
            if pd.isnull(token.eth_contract_address):
                print(f"no eth_contact_address for {token.identifier} skipping extraction...")
                continue
            req = OHLCPricesRequest(
                token_address=token.eth_contract_address,
                from_timestamp=date_start,
                until_timestamp=date_end
            )

            df_history = self.convert_eth_history_to_df(
                data=get_OHLC_price_history(req)['data']
            )
            df_history['token_id'] = token.id # inject our id col
            upsert_token_price_history(df_history=df_history , token_id=token.id)

            
    def convert_eth_history_to_df(self , data : dict)-> pd.DataFrame:
        date_cols = ['date_open','date_close']
        dtype = {
            'price_open' : 'Float64',
            'price_close' : 'Float64',
            'price_high' : 'Float64',
            'price_low' : 'Float64',
            'volume' : 'Float64',
            'num_trades' : 'Int64',
        # 'chain' : 'string',
            #'token_name' : 'string'
        }
        df = pd.DataFrame.from_records(data).drop(['timestamp_open','timestamp_close'],axis=1)
        df = df.astype(dtype)

        for col in date_cols:
            df[col] = df[col].apply(lambda x : pd.to_datetime(x).replace(tzinfo=None))


        return df
            