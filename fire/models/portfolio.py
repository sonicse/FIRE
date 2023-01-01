from datetime import datetime

from sqlmodel import (
    SQLModel,
)


class PortfolioTicker(SQLModel, table=False):
    ticker: str
    count: int
    price: float
    last_trade: datetime
