from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from sqlalchemy import create_engine
from cryptoTracker.db.postgres import LocalPostgresConnection  
import json 
import os

"""

    Contains methods to connect to local pg database for storing data...

"""
_POSTGRES_DB : LocalPostgresConnection = None

def init_pg_db(**engine_kwargs):
    global _POSTGRES_DB
    if(_POSTGRES_DB is not None):
        print("postgres db already initialised")
    else:
        print('initialising postgres db')
        _POSTGRES_DB = LocalPostgresConnection(**engine_kwargs)

def get_pg_db() -> LocalPostgresConnection:
    global _POSTGRES_DB
    if(_POSTGRES_DB is None):
        LocalPostgresConnection()
    return _POSTGRES_DB
