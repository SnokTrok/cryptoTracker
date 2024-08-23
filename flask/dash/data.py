
import json
import dateutil.tz
from rich import print
import pytz
import dateutil
import pandas as pd
from pandera import check_input , check_output
from cryptoTracker.application.queries.token import (
    get_tokens , get_price_history
)
from cryptoTracker.application.queries.exchange import (
    get_exhange_tokens , get_price_history as get_exchange_price_history
)
from cryptoTracker.flask.dash.schemas.data import (
    binance_kline_message_schema
)
from cryptoTracker.application.utils import empty_dataframe_like

#----------------------------

token_id = 11
exchange_token_id = 1
websockets = []
exchange_data = {}
exchange_id_map = {} #mapping binance symbol onto id

#---------------------------

def load_exchange_id_map() -> dict[int , dict]:
    """
        Load our excahnge token table and convert to id lookup...
    """
    global exchange_id_map
    df_exch_tokens = get_exhange_tokens()
    return {row.name : int(row.id) for row in df_exch_tokens.itertuples()}


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
        }
    return token_data


def append_binance_live_exch(df : pd.DataFrame , id : int):
    global exchange_data
    if id not in exchange_data.keys():
        # isert new symbol into pg , generate id and append ...
        raise ValueError(f"{id} Does not exist within exchange data mapping , should it be added?")
    else : exchange_data[id]['data'] = pd.concat([exchange_data[id]['data'] , df])

    exchange_data[id]['data'] = exchange_data[id]['data'].drop_duplicates(subset=['date_close'],keep='last')
    exchange_data[id]['data'].reset_index()


def on_binance_kline_message(message)-> pd.DataFrame:
    data = json.loads(message)['data']
    # check kline closed
    # if data['k']['x'] == False:
    #     print("Candle not closed , skipping...")
    #     return None
    
    df = pd.DataFrame.from_records([data['k']])
    df=df.rename({
        't' : 'date_open',
        'T' : 'date_close',
        "s" : 'symbol',
        'i' : 'interval',
        'o' : 'price_open',
        'c' : 'price_close',
        'h' : 'price_high',
        'l' : 'price_low',
        'n' : 'num_trades'
    },axis=1)
    df=df.astype({
        "symbol" : 'string',
        'interval' : 'string',
        'price_open' : 'Float64',
        'price_close' :'Float64',
        'price_high' : 'Float64',
        'price_low' : 'Float64',
        'num_trades' : 'Int64'
    })

    parse_epoch  = ['date_open' , 'date_close']

    for col in parse_epoch:
        df[col] = (
            df[col].apply(lambda x : pd.to_datetime(x,unit='ms')
                .tz_localize(pytz.utc)
                .astimezone(tz=dateutil.tz.gettz('Europe/London')))
        )

    append_binance_live_exch(df=df , id=exchange_id_map[data['s']])


# region----------- GET/SET------------

def get_current_token_id() -> int:
    global token_id
    return token_id

def set_current_token_id(id : int):
    global token_id
    token_id = id
    return token_id

def get_current_exhange_token_id() -> int:
    global exchange_token_id
    return exchange_token_id

def set_current_exchange_token_id(id : int):
    global exchange_token_id
    exchange_token_id = id
    return exchange_token_id

# endregion. ---------------------------

# init here

exchange_id_map = load_exchange_id_map()
exchange_data = {id : {"name" : name , 'data' : empty_dataframe_like(binance_kline_message_schema)} for name, id in exchange_id_map.items()}

token_data = load_price_history_data()

print(exchange_data)