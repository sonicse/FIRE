import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncConnection
from fire.dependencies.database import get_engine, AsyncEngine


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def connection() -> AsyncConnection:
    engine: AsyncEngine = await get_engine()
    async with engine.connect() as connection:
        yield connection
        await connection.rollback()
