from .base import BaseRepository
from fire.models.trade import Trade, TradeCreate


class TradeRepository(BaseRepository[Trade, TradeCreate]):
    table = Trade
