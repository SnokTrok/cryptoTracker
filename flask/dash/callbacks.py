
from dash.dependencies import Output , Input , State
import pandas as pd
from .figures.utils import (
    generate_candlestick_price_history_graph,
    generate_line_price_history_graph,
    generate_kline_live_binance_graph
)


def init_callbacks(dash_app):

    from .data import (
        token_data,
        exchange_data,
        exchange_id_map,
        get_current_token_id,
        set_current_token_id,
        get_current_exhange_token_id,
        set_current_exchange_token_id,
        on_binance_kline_message
    )

    @dash_app.callback(
            Output('static-price-history-candle-graph' ,'figure'),
            Output('static-price-history-line-graph' ,'figure'),
            Input('dd-token-select', 'value'),
            Input("rs-interval-filter" , 'value')
        )
    def change_token(token_id , date_range):# , start_date , end_date):

        token_id = set_current_token_id(token_id)

        df_history = token_data[token_id]['price_history']

        date_start = date_range[0] if date_range[0] < date_range[1] else date_range[1]
        date_end = date_range[1] if date_range[0] < date_range[1] else date_range[0]

        df_history = token_data[token_id]['price_history']

        date_start = pd.to_datetime(df_history.date_open.min() + pd.Timedelta(days=date_start))
        date_end = pd.to_datetime(df_history.date_open.min() + pd.Timedelta(days=date_end))

        print(f'{date_start} - {date_end}')
        date_mask = (
            df_history.date_open.ge(date_start) & df_history.date_close.le(date_end)
        )
        df_filtered = df_history.loc[date_mask]

        # build graphs
        candle_fig = generate_candlestick_price_history_graph(df_history=df_filtered,token_name=token_data[token_id]['token_name'],token_identifier='')
        line_fig = generate_line_price_history_graph(df_history=df_filtered,token_name=token_data[token_id]['token_name'],token_identifier='')
        return candle_fig , line_fig
    


    # region ------ INTERVAL---------------------

    @dash_app.callback(
            Output('live-binance-kline-graph','figure'),
            Input('ws-binance-live-dex','message')
    )
    def update_kline_binance_exchange_layout(message):
        """
            Contains elements for live information eg from binance websockets,

            since this data is streamed initialize as empty , run on interval tick.
        """
        exch = exchange_data[get_current_exhange_token_id()]
        data = exch['data']
        if message == None:
            print("no kline data to display...")
            return generate_kline_live_binance_graph(df_data=data,title=f'{exch["name"]} live price')
        on_binance_kline_message(message=message['data'])

        figure = generate_kline_live_binance_graph(df_data=data,title=f'{exch["name"]} live price')
        return figure


# endregion. --------------------------------
    

    