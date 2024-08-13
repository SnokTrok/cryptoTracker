
import pandas as pd
from cryptoTracker.application.queries.token import (
    get_tokens , get_price_history
)

token_id = 11

def load_price_history_data() ->  dict[int , dict]:
    """
        Returns token_info : price_history

        static dataframe from whenever we have the most updated history data for.
    """
    print("loading data ...")
    tokens , _ = get_tokens()

    token_data = {
    }
    for t in tokens.itertuples():
        token_data[t.id] = {
            "token_name" : f'{t.name} ({t.identifier})',
            "price_history" : get_price_history(token_id=t.id),
            "live_price" : pd.DataFrame({
                "timestamp" : [],
                'price' : []
            }).astype({
                'timestamp' : 'datetime64[ns]',
                'price' : 'Float64'
            })
        }
    return token_data

token_data = load_price_history_data()



def get_current_token_id() -> int:
    global token_id
    return token_id

def set_current_token_id(id : int):
    global token_id
    token_id = id
    return token_id