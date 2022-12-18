import pytest

from fire.models.trade import TradeCreate, TradeAction
from fire.repositories.trade import TradeRepository
from fire.repositories.errors import NotFoundError


@pytest.mark.asyncio
async def test_create(trade_repository: TradeRepository) -> None:
    trade_id = await trade_repository.create(
        TradeCreate(
            ticker='test',
            action=TradeAction.BUY,
            count=2,
            price=10,
        ),
    )
    assert trade_id


@pytest.mark.asyncio
async def test_delete(trade_repository: TradeRepository, create_trade) -> None:
    trade_created = await create_trade(
        ticker='test',
        action=TradeAction.BUY,
        count=2,
        price=10,
    )
    await trade_repository.delete(id=trade_created)
    try:
        await trade_repository.get(id=trade_created)
    except Exception as exc:
        assert isinstance(exc, NotFoundError)


@pytest.mark.asyncio
async def test_delete_notfound(trade_repository: TradeRepository) -> None:
    try:
        await trade_repository.delete(id=-1)
    except Exception as exc:
        assert isinstance(exc, NotFoundError)
    # assert get NotFound


@pytest.mark.asyncio
async def test_get(trade_repository: TradeRepository, trade: int) -> None:
    trade_data = await trade_repository.get(id=trade)
    assert trade_data.id == trade


@pytest.mark.asyncio
async def test_update(trade_repository: TradeRepository, trade: int) -> None:
    await trade_repository.update(
        trade,
        values= {
            'ticker': 'updated',
            'action': TradeAction.SELL,
            'count': 3,
            'price': 33,
        }
    )
    trade_data = await trade_repository.get(id=trade)
    assert trade_data.ticker == 'updated'
    assert trade_data.action == TradeAction.SELL
    assert trade_data.count == 3
    assert trade_data.price == 33


@pytest.mark.asyncio
async def test_filter(trade_repository: TradeRepository, trade: int) -> None:
    data = [item async for item in trade_repository.filter()]
    assert data[0].id == trade
