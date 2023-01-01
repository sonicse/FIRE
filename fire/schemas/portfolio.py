from datetime import datetime
from typing import List
from pydantic import BaseModel, Extra


class TickerSchema(BaseModel):
    ticker: str
    count: int
    price: float
    last_trade: datetime


class PortfolioResponse(BaseModel):
    count: int
    items: List[TickerSchema]

    class Config:
        extra = Extra.forbid