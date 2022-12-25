from fastapi import Depends

from fire.dependencies.database import get_repository
from fire.repositories.trade import TradeRepository
from fire.services.trade import TradeService


async def get_trade_service(
        trade_repository: TradeRepository = Depends(get_repository(TradeRepository))
) -> TradeService:
    return TradeService(trade_repository=trade_repository)
