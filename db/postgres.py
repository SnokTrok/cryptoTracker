from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
from sqlalchemy import create_engine
from cryptoTracker.application.utils import get_secret


class LocalPostgresConnection():
    def __init__(self , **engine_kwargs) -> None:

        if 'echo' not in engine_kwargs:
            engine_kwargs['echo'] = False
        if 'pool_pre_ping' not in engine_kwargs:
            engine_kwargs['pool_pre_ping'] = True

        self.engine = create_engine(self.get_conn_string(), **engine_kwargs)
        self.session_factory = sessionmaker(
            bind=self.engine
            # autocommit=True
        )
        self.Session = scoped_session(self.session_factory)

    def get_conn_string(self) -> str:
        db_creds = get_secret('postgres')
        db_user = db_creds['username']
        db_pass = db_creds['password']
        port = db_creds['port']
        db_database =  db_creds['database']
        host = db_creds['host']

        print(f'connecting to {host}:{port}')
        return f"postgresql+psycopg2://{db_user}:{db_pass}@{host}:{port}/{db_database}?sslmode=allow"
    

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
