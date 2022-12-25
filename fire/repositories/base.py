from typing import Any, AsyncGenerator, Dict, Generic, Optional, Type, TypeVar

from sqlalchemy import delete, desc, func, insert, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import text
from sqlmodel import SQLModel, update

from fire.repositories.errors import (
    ForeignKeyViolationError,
    NotFoundError,
    UniqueViolationError,
    RepositoryError
)
from fire.models.base import BaseModel

Table = TypeVar('Table', bound=BaseModel)
TableCreate = TypeVar('TableCreate', bound=SQLModel)


class BaseRepository(Generic[Table, TableCreate]):

    table: Type[Table]

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection
        self.all_columns = [text(c_attr.key) for c_attr in self.table._sa_class_manager.mapper.column_attrs]

    async def count(self) -> int:
        statement = select(func.count(self.table.id))
        count: int = await self.connection.scalar(statement)
        return count

    async def get(self, id: int, connection: Optional[AsyncConnection] = None) -> Table:
        statement = select(self.table).where(self.table.id == id)
        return await self._process_crud_statement(statement)

    async def create(
        self, entity: TableCreate, connection: Optional[AsyncConnection] = None
    ) -> int:
        statement = insert(self.table).values(entity.dict())
        try:
            result = await (connection or self.connection).execute(statement)
        except IntegrityError as exc:
            raise UniqueViolationError() from exc
        item_id = result.lastrowid
        return item_id

    async def update(
        self,
        id: int,
        values: Dict[str, Any],
        connection: Optional[AsyncConnection] = None,
    ) -> Table:
        statement = (
            update(self.table)
            .where(self.table.id == id)
            .values(**values, updated_at=func.now())
        )
        try:
            result_cursor = await (connection or self.connection).execute(statement)
        except SQLAlchemyError as exc:
            raise exc
        if result_cursor.rowcount != 1:
            raise NotFoundError()

    async def delete(
        self, id: int, connection: Optional[AsyncConnection] = None
    ) -> Table:
        statement = (
            delete(self.table).where(self.table.id == id)
        )
        try:
            result_cursor = await (connection or self.connection).execute(statement)
        except SQLAlchemyError as exc:
            raise exc
        if result_cursor.rowcount != 1:
            raise NotFoundError()

    async def filter(
        self,
        expression=None,
        order=None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        connection: Optional[AsyncConnection] = None,
    ) -> AsyncGenerator[Table, None]:
        if order is None:
            order = desc(self.table.id)
        statement = select(self.table).order_by(order)
        if expression is not None:
            statement = statement.where(expression)
        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(limit)

        rows = await (connection or self.connection).stream(statement)
        async for row in rows:
            obj: Table = self.table.from_orm(row)
            yield obj

    async def _process_crud_statement(
            self,
            statement,
            connection: Optional[AsyncConnection] = None
    ) -> Table:
        try:
            rows = await (connection or self.connection).execute(statement)
        except IntegrityError as exc:
            raise UniqueViolationError() from exc
        item = rows.first()
        if item is not None:
            obj: Table = self.table.from_orm(item)
            return obj
        raise NotFoundError()
