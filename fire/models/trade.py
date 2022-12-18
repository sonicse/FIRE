from enum import Enum

from sqlmodel import (
    SQLModel,
)

from .base import BaseModel


class TradeAction(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class TradeBase(SQLModel, table=False):
    ticker: str
    action: TradeAction
    count: int
    price: float


class Trade(BaseModel, TradeBase, table=True):
    pass


class TradeCreate(TradeBase):
    pass
