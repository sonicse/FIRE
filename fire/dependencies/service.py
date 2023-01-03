from fastapi import Depends
import httpx
import requests

from fire.dependencies.database import get_repository
from fire.repositories.trade import TradeRepository
from fire.services.trade import TradeService
from fire.services.stock import StockService


async def get_trade_service(
        repository: TradeRepository = Depends(get_repository(TradeRepository))
) -> TradeService:
    return TradeService(trade_repository=repository)


def get_http_client():
    # return httpx.Client(verify=False)
    http_client = requests.Session()
    http_client.verify = False
    return http_client


async def get_stock_service(
        http_client=Depends(get_http_client)
) -> StockService:
    return StockService(http_client=http_client)
