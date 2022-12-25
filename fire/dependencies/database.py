from typing import AsyncGenerator, Optional, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncConnection,
    create_async_engine,
)
from fire.conf.settings import settings
from fire.repositories.base import BaseRepository

engine: AsyncEngine = create_async_engine(url=settings.DATABASE_URL, echo=settings.DATABASE_ECHO, future=True)


async def get_engine() -> AsyncEngine:
    if engine is not None:
        return engine
    raise RuntimeError("Application not started.")


async def get_connection(
    engine: AsyncEngine = Depends(get_engine),
) -> AsyncGenerator[AsyncConnection, None]:
    # async with engine.begin() as connection:
    async with engine.connect() as connection:
        yield connection


def get_repository(repository: Type[BaseRepository]):
    async def wrapper(
        connection: AsyncConnection = Depends(get_connection),
    ) -> BaseRepository:
        instance = repository(connection=connection)
        return instance
    return wrapper