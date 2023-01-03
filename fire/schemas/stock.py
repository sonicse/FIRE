from datetime import datetime
from typing import List
from pydantic import BaseModel, Extra


class StockTicker(BaseModel):
    ticker: str
    count: int
    price: float
    last_trade: datetime


class StockResponse(BaseModel):
    count: int
    items: List[StockTicker]

    class Config:
        extra = Extra.forbid