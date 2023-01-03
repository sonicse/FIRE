from fastapi import APIRouter, Depends

from fire.dependencies.service import get_stock_service
from fire.services.stock import StockService
from fire.schemas.stock import (
    StockResponse,
    StockTicker,
)
from fire.repositories.errors import (
    NotFoundError,
)
from .errors import (
    NotFoundHTTPException,
)


router = APIRouter(tags=['stock'])


# @router.get(
#     '/',
#     name='stock:list',
#     response_model=StockResponse,
#     summary='Portfolio',
# )
# async def list(
#     service: StockService = Depends(get_stock_service),
# ) -> StockResponse:
#     items = [item async for item in service.list()]
#     return StockResponse(
#         count=len(items),
#         items=items,
#     )


@router.get(
    '/{ticker}',
    name='stock:get',
    # response_model=StockTicker,
    summary='Get Portfolio Ticker'
)
async def get(
    ticker: str,
    service: StockService = Depends(get_stock_service),
) -> StockTicker:
    try:
        return await service.info(ticker=ticker)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {ticker} not found') from exc


@router.get(
    '/{ticker}/history',
    name='stock:get',
    # response_model=StockTicker,
    summary='Get Portfolio Ticker'
)
async def get(
    ticker: str,
    period: str,
    start: str,
    end: str,
    service: StockService = Depends(get_stock_service),
) -> StockTicker:
    try:
        return await service.history(ticker=ticker, period=period, start=start, end=end)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {ticker} not found') from exc


@router.get(
    '/{ticker}/actions',
    name='stock:get',
    # response_model=StockTicker,
    summary='Get Portfolio Ticker'
)
async def get(
    ticker: str,
    service: StockService = Depends(get_stock_service),
) -> StockTicker:
    try:
        return await service.actions(ticker=ticker)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {ticker} not found') from exc


@router.get(
    '/{ticker}/quarterly_financials',
    name='stock:get',
    # response_model=StockTicker,
    summary='Get Portfolio Ticker'
)
async def get(
    ticker: str,
    service: StockService = Depends(get_stock_service),
) -> StockTicker:
    try:
        return await service.quarterly_financials(ticker=ticker)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {ticker} not found') from exc


@router.get(
    '/{ticker}/recommendations',
    name='stock:get',
    # response_model=StockTicker,
    summary='Get Portfolio Ticker'
)
async def get(
    ticker: str,
    service: StockService = Depends(get_stock_service),
) -> StockTicker:
    try:
        return await service.recommendations(ticker=ticker)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {ticker} not found') from exc
