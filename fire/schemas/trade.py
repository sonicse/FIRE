from datetime import datetime
from typing import Annotated, List, Optional
from pydantic import BaseModel, Extra

from fire.models.trade import TradeAction


class TradeSchema(BaseModel):
    id: int
    ticker: str
    action: TradeAction
    count: int
    price: float
    created_at: datetime
    updated_at: datetime


class TradeListResponse(BaseModel):
    count: int
    items: List[TradeSchema]

    class Config:
        extra = Extra.forbid


class TradeCreateRequest(BaseModel):
    ticker: str
    action: TradeAction
    count: int
    price: float

    class Config:
        extra = Extra.forbid
