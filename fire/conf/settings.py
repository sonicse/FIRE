from typing import Dict, List, Set, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    VERSION: str = '0.0.1'

    API_PREFIX: str = '/api/v1'
    API_TITLE: str = 'FIRE backend'

    DATABASE_URL: str = 'sqlite+aiosqlite:///C:/Users/AAnikeev/PycharmProjects/FIRE/data/database_2022.12.25.db'
    DATABASE_ECHO: bool = True


settings = Settings('.env')
