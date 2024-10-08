from datetime import datetime
import pandas as pd
import numpy as np
from cryptoTracker.application.queries.token import (
    get_tokens , validate_token_info , get_price_history
)
from cryptoTracker.application.extracts.coin_price_history import CoinPriceExtractor

import plotly.graph_objects as go
import plotly.io as pio  
import plotly.express as px

pio.renderers.default = 'iframe'

"""
    Utils functions for generating data visualisation figures...
"""


# region -------------------GRAPHS--------------

def generate_price_history_charts(token_id : int):
    df_token , _ = get_tokens(token_id=token_id)
    token_name = list(df_token.name)[0]
    token_identifier = df_token.iloc[0].identifier

    df_history = get_price_history(token_id=token_id)

    candlestick_graph = generate_candlestick_price_history_graph(df_history=df_history,
                                                                 token_name=token_name,
                                                                 token_identifier=token_identifier)
    line_graph = generate_line_price_history_graph(df_history=df_history,
                                                   token_name=token_name,
                                                   token_identifier=token_identifier)
    return candlestick_graph , line_graph


def generate_candlestick_price_history_graph(df_history : pd.DataFrame, token_name = None,
                                             token_identifier = None):
    """
        constructs plotly graph , from history 
    """
    fig = go.Figure(data=[go.Candlestick(x=df_history['date_open'],
                open=df_history['price_open'],
                high=df_history['price_high'],
                low=df_history['price_low'],
                close=df_history['price_close'])])
    fig.update_layout(title=f'{token_name} ({token_identifier})')
    return fig


def generate_line_price_history_graph(df_history : pd.DataFrame ,
                                    token_name : str,
                                    token_identifier : str):
    df_history = df_history.sort_values('date_open',ascending=True)
    fig = px.line(df_history, x="date_open", y="price_open", title=f'{token_name} ({token_identifier})')
    return fig


def generate_kline_live_binance_graph(df_data : pd.DataFrame , title : str):
    """
        This is called upon interval component tick , and fed data from data.py
    """
    # fig = go.Figure(data=[go.Candlestick(x=df_data['date_open'],
    #             open=df_data['price_open'],
    #             high=df_data['price_high'],
    #             low=df_data['price_low'],
    #             close=df_data['price_close'])])
    
    # or plotting close price only ...
    fig = px.area(df_data , x='date_close' , y='price_close')

    fig.update_layout(title=title)

    return fig

# endregion.




