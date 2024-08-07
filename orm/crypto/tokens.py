
import pandas as pd
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
    Tables related to token information.
"""

# region ----------- GENERIC------------------------

class Token(Base):
    __tablename__ = 'token'
    __table_args__ = {'schema' : 'crypto'}

    id = Column(BigInteger,primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False) # verbose name
    identifier = Column(String(10), nullable=False) # coin code eg , BTC , ETH etc ...
    chain = Column(String(10),nullable=True) # for example bitcoin exists standalone , but lots of coins on ETH chain
    eth_contract_address = Column(String(100) , nullable=True)
    price_history = relationship('TokenPriceHistory',back_populates="token")
        


class TokenPriceHistory(Base):
    __tablename__ = 'token_price_history'
    __table_args__ = {'schema' : 'crypto'}

    # PK on token_id , interval start should be pretty consistent, also index on this / order by ...
    token_id = Column(BigInteger,ForeignKey("crypto.token.id",onupdate='CASCADE',ondelete='CASCADE'),primary_key=True)
    date_open = Column(DateTime,primary_key=False)
    date_close = Column(DateTime,nullable=False)
    price_open = Column(Numeric,nullable=True)
    price_close = Column(Numeric,nullable=True)
    price_high = Column(Numeric,nullable=True)
    price_low = Column(Numeric,nullable=True)
    volume = Column(Numeric,nullable=True)
    num_trades = Column(Integer,nullable=True)
    periodicity = Column(String(3),nullable=False)

    token = relationship("Token",foreign_keys=[token_id],back_populates='price_history')


# endregion. ----------------------------------------------