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


def generate_token_info_html(selected_token_id : int = None) -> str:
    """
        Will be injected to html when app loaded into token_widget

         <form action="/change-token" method="post">
            <input type="hidden" name="token_id" value=1>
            <button type="submit">Token Name</button>
        </form>
    """
    df_tokens , _ = get_tokens()
    data = []
    for token in df_tokens.itertuples():
        if selected_token_id == token.id:
            s = f"<option value={token.id} selected>{token.name} ({token.identifier})</option>"
        else : s = f"<option value={token.id}>{token.name} ({token.identifier})</option>"
        data.append(s)
    data = "\n".join(data)
    template = f"""
        <form action="/change-token" method="post" id="token_dropdown_form">
            <label for="token_dropdown">Select a token view:</label>
            <select id="token_dropdown" name="token_id" onChange=this.form.submit()>
            {data}
            </select>
        </form> 
    """
    return template



