from typing import Dict, List, Set, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite+aiosqlite:///C:/Users/AAnikeev/PycharmProjects/FIRE/data/database.db'
    DATABASE_ECHO: bool = True


settings = Settings('.env')
