from fastapi import APIRouter, Depends, status

from fire.models.trade import Trade
from fire.dependencies.service import get_trade_service
from fire.services.trade import TradeService
from fire.schemas.trade import (
    TradeCreateRequest,
    TradeListResponse,
    TradeSchema,
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


router = APIRouter(tags=['trades'])


@router.get(
    '/',
    name='trade:list',
    response_model=TradeListResponse,
    summary='Get trades',
)
async def list_trades(
    trade_service: TradeService = Depends(get_trade_service),
) -> TradeListResponse:
    items = [item async for item in trade_service.list_trades()]
    return TradeListResponse(
        count=len(items),
        items=items,
    )


@router.post(
    '/',
    name='trade:create',
    status_code=status.HTTP_201_CREATED,
    response_model=TradeSchema,
    summary='Create trade',
)
async def create(
    request: TradeCreateRequest,
    trade_service: TradeService = Depends(get_trade_service),
) -> TradeSchema:
    try:
        trade_id = await trade_service.create_trade(
            request.dict()
        )
        trade_entity: Trade = await trade_service.get_trade_by_id(trade_id=trade_id)
    except UniqueViolationError as exc:
        raise RequestValidationHTTPException(
            detail=[
                RequestValidationDetail(
                    location=['body', 'title'],
                    message='Dataset with this title already exists',
                    type=None,
                )
            ]
        ) from exc
    return trade_entity


@router.get(
    '/{id}',
    name='dataset:get',
    response_model=TradeSchema,
    summary='Get trade'
)
async def get(
    id: int,
    trade_service: TradeService = Depends(get_trade_service),
) -> TradeSchema:
    try:
        return await trade_service.get_trade_by_id(trade_id=id)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {id} not found') from exc


@router.delete(
    '/{id}',
    name='dataset:delete',
    response_model=None,
    summary='Delete trade',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    id: int,
    trade_service: TradeService = Depends(get_trade_service),
) -> None:
    try:
        return await trade_service.delete_trade(trade_id=id)
    except NotFoundError as exc:
        raise NotFoundHTTPException(detail=f'Entity with id = {id} not found') from exc
    except ForeignKeyViolationError as exc:
        raise RelatedObjectsExistHTTPException(
            detail='Can\'t delete dataset: related objects exists'
        ) from exc

