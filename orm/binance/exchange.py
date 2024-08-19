from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, BigInteger,
    String, Boolean,
    TIMESTAMP,
    Column, ForeignKey, Table, UniqueConstraint, Index, DateTime , Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy import func

from cryptoTracker.orm.base import Base

"""
    Binance doesnt contain live price data for all crypto's but it does allow you to stream conversion prices between coins,

    EG using websocket api to stream candelstick charting data for WBTCUSDT will return the conversion from wrapped bit coin (present on ethereum blockchain)
    to USDT Tether (almost 1:1 with real world USD) , meaning to plot live charting data we would need to figure out exactly what data to be storing

    in this case for POC I will only look at storing coin->USDT in a real world trading bot implementation however it would be a good idea to look at all conversions
    and create  weigthing algorithm based on coin_activity , conversion_rate (relative) , prediction_scores (from multiple ML implementations I would like to try 
    normalizing the result weighting based on accuracy scores)

    this module will contain all the tables housing data colected via the binance api(s)
"""



class TokenExchangeCandlestickHistory(Base):
    __table_name__ = 'token_exchange_candlestick_history'
    __tableargs__ = {'schema' : 'exchange'}

    symbol = Column(String(10) , primary_key=True)
    date_open = Column(DateTime,primary_key=True)
    date_close = Column(DateTime,nullable=False)
    price_open = Column(Numeric,nullable=True)
    price_close = Column(Numeric,nullable=True)
    price_high = Column(Numeric,nullable=True)
    price_low = Column(Numeric,nullable=True)
    num_trades = Column(Integer , nullable=False)

    