from pandera import DataFrameSchema,Column


binance_kline_message_schema = DataFrameSchema(
    columns={
    'symbol' : Column('string') ,
    'price_open' : Column('Float64' , nullable=False),
    'price_close' : Column('Float64' , nullable=False),
    'price_low' : Column('Float64' , nullable=False),
    'price_high'  : Column('Float64', nullable=False),
    'date_open' : Column('datetime64[ns]',nullable=False),
    'date_close' : Column('datetime64[ns]', nullable=False)
    },
    strict=True,
    coerce=False
)