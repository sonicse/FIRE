from typing import AsyncGenerator

from fire.models.trade import Trade, TradeCreate
from fire.repositories.trade import TradeRepository


class TradeService:
    def __init__(self, trade_repository: TradeRepository):
        self.trade_repository: TradeRepository = trade_repository

    async def create_trade(self, trade_input: dict) -> int:
        async with self.trade_repository.connection.begin() as transaction:
            trade_create = TradeCreate.parse_obj(trade_input)
            trade_id = await self.trade_repository.create(entity=trade_create)
            return trade_id

    async def delete_trade(self, trade_id: int) -> None:
        async with self.trade_repository.connection.begin() as transaction:
            await self.trade_repository.delete(id=trade_id)

    async def update_trade(self, trade_id: int, trade_input: dict) -> None:
        async with self.trade_repository.connection.begin() as transaction:
            await self.trade_repository.update(id=trade_id, values=trade_input)

    async def get_trade_by_id(self, trade_id: int) -> Trade:
        return await self.trade_repository.get(id=trade_id)

    async def list_trades(self) -> AsyncGenerator[Trade, None]:
        async for trade in self.trade_repository.filter():
            yield trade
