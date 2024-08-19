
import pandas as pd
import websocket
from cryptoTracker.application.queries.token import (
    get_tokens , get_price_history
)

token_id = 11
websockets = []
exchange_data = {}

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

token_data = load_price_history_data()

def get_current_token_id() -> int:
    global token_id
    return token_id

def set_current_token_id(id : int):
    global token_id
    token_id = id
    return token_id


def open_binance_websockets():
    global websockets
    global exchange_data
    # currency websocket endpoints to subscribe to 
    subscribed = ['WBTCUSDT', 'WBTCETH']

    # kline_1m -> per min updated stream of data 
    subscribed = "/".join([coin.lower() + '@kline_1m' for coin in subscribed])
    socket = "wss://stream.binance.com:9443/stream?streams=" + subscribed
    ws = websocket.WebSocketApp(socket, on_message=on_binance_kline_message)
    ws.run_forever()
    websockets.append(ws)

def close_binance_websockets():
    global websockets
    for socket in websockets:
        socket.close()


def append_binance_live_exch(df : pd.DataFrame , symbol : str):
    global exchange_data
    if symbol not in exchange_data.keys():
        exchange_data[symbol] = df
    else : exchange_data[symbol] = pd.concat([exchange_data[symbol] , df])

# region------------- WEBSOCKET ------------------

def on_binance_kline_message(message) -> pd.DataFrame:
    """
        for resp formatting see : https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Kline-Candlestick-Streams
    """
    data = message['data']
    
    # check kline closed
    if data['k']['x'] == False:
        return None
    
    df = pd.DataFrame.from_dict(data['k'],orient='records').rename({
        't' : 'date_open',
        'T' : 'date_close',
        "s" : 'symbol',
        'i' : 'interval',
        'o' : 'price_open',
        'c' : 'price_close',
        'h' : 'price_high',
        'l' : 'price_low',
        'n' : 'num_trades'
    }).astype({
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
        df[col] = df[col].apply(lambda x : pd.to_datetime(x).replace(tzinfo=None))

    append_binance_live_exch(df=df , symbol=list(df.symbol)[0])

    # here we upsert the data into postgres , we may as well start storing historical reprensetation using real merics?
