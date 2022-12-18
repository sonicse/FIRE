import re
from datetime import datetime
from typing import Optional

from pydantic import ConstrainedStr
from slugify import slugify
from sqlalchemy import func
from sqlmodel import Field, SQLModel


class StrictSlugField(ConstrainedStr):
    """
    Used as s3/lakefs bucket names.
    """

    regex = re.compile(r'^[a-zA-Z0-9-]{2,32}$')


class VersionSlugField(ConstrainedStr):
    regex = re.compile(r'^[a-zA-Z0-9-]{2,16}$')


class TitleStringField(ConstrainedStr):
    strip_whitespace = True
    min_length = 2
    max_length = 32

    @property
    def slug(self) -> str:
        return slugify(text=self, max_length=32, separator='-', lowercase=True)


class BaseModel(SQLModel):
    id: int = Field(primary_key=True)

    created_at: Optional[datetime] = Field(
        sa_column_kwargs={'server_default': func.now()}
    )
    updated_at: Optional[datetime] = Field(
        sa_column_kwargs={'server_default': func.now()}
    )
