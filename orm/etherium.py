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
    Contains db models for ETH tables , built using a relational model for convenience.
"""


class UserInfo(Base):
    __tablename__ = 'user_info'
    __table_args__ = {'schema': 'crypto'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    hash_id = Column(String(255), nullable=False)
    blockchain = Column(String(10), nullable=False)

    mined_blocks = relationship("EthereumTransactionBlocks", back_populates="miner")
    sent_transactions = relationship("EthereumTransactionHistory", foreign_keys="[EthereumTransactionHistory.from_id]", back_populates="from_user")
    received_transactions = relationship("EthereumTransactionHistory", foreign_keys="[EthereumTransactionHistory.to_id]", back_populates="to_user")


class EthereumTransactionHistory(Base):
    __tablename__ = 'ethereum_transaction_history'
    __table_args__ = {'schema': 'crypto'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    block_id = Column(BigInteger, ForeignKey('crypto.ethereum_transaction_blocks.id', onupdate='CASCADE', ondelete='CASCADE'))
    from_id = Column(BigInteger, ForeignKey('crypto.user_info.id', onupdate='CASCADE', ondelete='CASCADE'))
    to_id = Column(BigInteger, ForeignKey('crypto.user_info.id', onupdate='CASCADE', ondelete='CASCADE'))
    amount = Column(String(200))
    transaction_number = Column(Integer, nullable=False)
    sent_at = Column(TIMESTAMP(timezone=False))
    created_at = Column(TIMESTAMP(timezone=False), server_default=func.now())

    block = relationship("EthereumTransactionBlocks", back_populates="transactions")
    from_user = relationship("UserInfo", foreign_keys=[from_id], back_populates="sent_transactions")
    to_user = relationship("UserInfo", foreign_keys=[to_id], back_populates="received_transactions")


class EthereumTransactionBlocks(Base):
    __tablename__ = 'ethereum_transaction_blocks'
    __table_args__ = {'schema': 'crypto'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    block_hash = Column(String(200), nullable=False)
    block_number = Column(String(100), nullable=False)
    block_index = Column(String(200))
    block_time = Column(DateTime, nullable=False)
    transaction_count = Column(Integer, nullable=False)
    gas_limit = Column(String(200), nullable=False)
    gas_used = Column(String(200), nullable=False)
    size_bytes = Column(String(200), nullable=False)
    miner_id = Column(BigInteger, ForeignKey('crypto.user_info.id'))

    miner = relationship("UserInfo", back_populates="mined_blocks")
    transactions = relationship("EthereumTransactionHistory", back_populates="block")


# endregion.