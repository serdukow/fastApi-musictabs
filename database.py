from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "sqlite:///sqlite.db",
    connect_args={'check_same_thread': False}
)


Session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False
)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()