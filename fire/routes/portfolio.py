from fastapi import APIRouter, Depends

from fire.dependencies.service import get_trade_service
from fire.services.trade import TradeService
from fire.schemas.portfolio import (
    PortfolioResponse,
    PortfolioTicker,
)
from fire.repositories.errors import (
    ForeignKeyViolationError,
    NotFoundError,
    UniqueViolationError,
)
from .errors import (
    NotFoundHTTPException,
    RelatedObjectsExistHTTPException,
    RequestValidationDetail,
    RequestValidationHTTPException,
)


router = APIRouter(tags=['portfolio'])


@router.get(
    '/',
    name='portfolio:list',
    response_model=PortfolioResponse,
    summary='Portfolio',
)
async def list(
    service: TradeService = Depends(get_trade_service),
) -> PortfolioResponse:
    items = [item async for item in service.portfolio()]
    return PortfolioResponse(
        count=len(items),
        items=items,
    )


@router.get(
    '/{ticker}',
    name='portfolio:get',
    response_model=PortfolioTicker,
    summary='Get Portfolio Ticker'
)
async def get(
    ticker: str,
    service: TradeService = Depends(get_trade_service),
) -> PortfolioTicker:
    try:
        return await service.get_ticker(ticker=ticker)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {ticker} not found') from exc
