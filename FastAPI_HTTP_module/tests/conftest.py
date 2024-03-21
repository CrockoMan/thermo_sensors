import pytest

from config import MODE
from database import engine, Base


@pytest.fixture
async def prepare_database():
    assert MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all(conn))
        await conn.run_sync(Base.metadata.create_all(conn))
