from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)
from fire.conf.settings import settings

engine: AsyncEngine = create_async_engine(url=settings.DATABASE_URL, echo=settings.DATABASE_ECHO, future=True)


async def get_engine() -> AsyncEngine:
    if engine is not None:
        return engine
    raise RuntimeError("Application not started.")
