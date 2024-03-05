from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///sqlite.db"
# engine = create_async_engine("sqlite+aiosqlite:///sqlite.db")
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine,
                                         class_=AsyncSession,
                                         expire_on_commit=False)


class Base(DeclarativeBase):
    pass

