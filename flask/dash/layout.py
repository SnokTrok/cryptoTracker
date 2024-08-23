from typing import Tuple
import asyncio
from datetime import datetime
from dash import dcc, html
from dash_extensions import WebSocket
import pandas as pd

from cryptoTracker.flask.dash.figures.utils import (
    generate_candlestick_price_history_graph,
    generate_line_price_history_graph,
    generate_kline_live_binance_graph,
)
from cryptoTracker.application.utils import empty_dataframe_like
from cryptoTracker.flask.dash.schemas.data import binance_kline_message_schema
from cryptoTracker.flask.dash.data import token_data , get_current_token_id , on_binance_kline_message


starting_token_id = get_current_token_id()
starting_data_filter = (datetime(2024,7,1),datetime(2024,8,1))


def load_dt_slider( date_min  : datetime, date_max : datetime) -> dcc.RangeSlider:
    """
        Constructs a slider using EPOCH integer ranges , but display as datetime conversions?
    """
    # remove time from datetime components
    date_min = date_min.date()
    date_max = date_max.date()

    start_date =starting_data_filter[0].date()
    end_date = starting_data_filter[1].date()
    # generate a series of days between min-max inclusive

    time_series = pd.date_range(date_min , date_max , freq='1d', inclusive='both')
    num_days = len(time_series)

    start_val = end_val = 0
    for i , dt in enumerate(time_series):
        if dt.date() == start_date:
            start_val = i
        if dt.date() == end_date:
            end_val = i 
            break

    return dcc.RangeSlider(
        min=1, max=num_days,
        id="rs-interval-filter",
        value=[start_val,end_val],
        marks={i:str(dt.date()) for i , dt in enumerate(time_series) if dt.month % 3 == 0 and dt.day == 1},
        allowCross=False,
        updatemode='drag'
    )


def load_static_price_history_graphs(df_history, token_info) -> html.Div:
    
    # get our data apply our filters and populate graph
    dt_slider = load_dt_slider(date_min=df_history.date_open.min(),date_max=df_history.date_close.max())
    filter_mask = (
        df_history.date_open.ge(pd.to_datetime(starting_data_filter[0])) & 
        df_history.date_close.le(pd.to_datetime(starting_data_filter[1]))
    )
    df_history = df_history.loc[filter_mask]

    candle_fig = generate_candlestick_price_history_graph(df_history=df_history,token_name=token_info['token_name'],token_identifier='')
    line_fig = generate_line_price_history_graph(df_history=df_history,token_name=token_info['token_name'],token_identifier='')

    candle_graph = dcc.Graph(figure=candle_fig, 
                             id='static-price-history-candle-graph',
                             style={'display': 'inline-block'})   

    line_graph = dcc.Graph(figure=line_fig, 
                           id='static-price-history-line-graph', 
                           style={'display': 'inline-block'})
    
    # build graph component using starting fig...
    return html.Div(children=[candle_graph , 
                              line_graph, 
                              dt_slider], 
                              id='static-price-history-div')


def build_graph_layout() -> html.Div:
    """
        Here we define our graph layout structures for token info 
    """
    token_info = token_data[starting_token_id]
    df_history = token_info["price_history"]
    price_history_div = load_static_price_history_graphs(df_history=df_history,
                                                         token_info=token_info)
    

    # for now just wrap this , but will add other fields into this div here specifically.
    return price_history_div


def load_token_dropdown() -> dcc.Dropdown:
    options = []
    for token_id , token_info in token_data.items():
        option = {
            "label" : token_info['token_name'],
            "value" : token_id  
        }
        options.append(option)

    return dcc.Dropdown(id='dd-token-select',options=options , value=1)


def load_dashboard_layout() -> html.Div:
    """
        Load our dashboard , loading any data needed before hand etc
    """
    
    layout = html.Div(id='dash-container',
                               children=[
                                   load_token_dropdown(),
                                   build_graph_layout(),
                                   build_live_exchange_layout()
                               ]
    )
    return layout

# region ---------------------------

def build_live_exchange_layout() -> html.Div:
    """
        Contains elements for live information eg from binance websockets,

        since this data is streamed initialize as empty , run on interval tick.
    """

    df_empty = empty_dataframe_like(schema=binance_kline_message_schema)
    figure = generate_kline_live_binance_graph(df_data=df_empty,title='WBTCUSDT live price')
    graph = dcc.Graph(
        figure=figure,
        id='live-binance-kline-graph',
        style={'display' : 'inline-block'}
    )

    # websocket connection...
    subscribed_symbols = ['WBTCUSDT']#, 'WBTCETH']

    # kline_1m -> per min updated stream of data 
    subscribed = "/".join([coin.lower() + '@kline_1m' for coin in subscribed_symbols])
    socket = "wss://stream.binance.com:9443/stream?streams=" + subscribed

    print(f"Listening to Binance kline_1m websockets for  : {subscribed_symbols} ...")

    return html.Div(children=[
            graph,
            WebSocket(url=socket,id='ws-binance-live-dex')
        ],
        id='div-live-binance',
    ) # can use this tag to toggle visibility


# endregion. --------------------------------