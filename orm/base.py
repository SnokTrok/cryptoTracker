from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, BigInteger,
    String, Boolean,
    TIMESTAMP,
    Column, ForeignKey, Table, UniqueConstraint, Index, DateTime , Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy import func

Base = declarative_base()
metadata = Base.metadata