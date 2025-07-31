from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(url=str(config.pg_db.dsn), echo=config.pg_db.is_echo)
session_maker = async_sessionmaker(engine, expire_on_commit=False)
