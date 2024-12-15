from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.engine import Engine
from datetime import datetime
import pytz
from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.SQLITE_URL,
    connect_args={
        "check_same_thread": False,
    },
    pool_pre_ping=True,
    pool_recycle=300,
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA timezone=':Asia/Shanghai'")
    cursor.close()


@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if statement.lower().startswith("insert"):
        now = datetime.now(pytz.timezone(settings.TIMEZONE))
        params = list(params)
        for i, param in enumerate(params):
            if isinstance(param, datetime) and param.tzinfo is None:
                params[i] = param.replace(tzinfo=pytz.timezone(settings.TIMEZONE))
        params = tuple(params)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
