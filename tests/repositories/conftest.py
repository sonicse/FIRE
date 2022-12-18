import pytest
from sqlalchemy.ext.asyncio import AsyncConnection
from fire.repositories.trade import TradeRepository
from fire.models.trade import Trade, TradeCreate, TradeAction


@pytest.fixture
def trade_repository(connection: AsyncConnection) -> TradeRepository:
    repository: TradeRepository = TradeRepository(connection=connection)
    return repository


@pytest.fixture
def create_trade(trade_repository: TradeRepository):
    async def wrapper(ticker: str, action: TradeAction, count: int, price: float):
        trade_id = await trade_repository.create(
            TradeCreate(
                ticker=ticker,
                action=action,
                count=count,
                price=price,
            ),
        )
        assert trade_id
        return trade_id
    return wrapper


@pytest.fixture
def delete_trade(trade_repository: TradeRepository):
    async def wrapper(trade_id: int):
        await trade_repository.delete(id=trade_id)
    return wrapper


@pytest.fixture(scope='function')
async def trade(create_trade, delete_trade):
    trade_created = await create_trade(
        ticker='conftest',
        action=TradeAction.BUY,
        count=5,
        price=20,
    )
    yield trade_created
    await delete_trade(trade_created)
