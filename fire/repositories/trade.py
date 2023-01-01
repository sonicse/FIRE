from typing import AsyncGenerator, Any

from sqlmodel import asc, select, func, text

from .base import BaseRepository
from fire.models.trade import Trade, TradeCreate
from fire.models.portfolio import PortfolioTicker


class TradeRepository(BaseRepository[Trade, TradeCreate]):
    table = Trade

    async def portfolio(self) -> AsyncGenerator[PortfolioTicker, None]:
        statement = text('''
select
ticker,
 sum(
     case
      when action = 'BUY' then count
      when action = 'SELL' then -count
     end
     ) as count,
 sum(
     case
      when action = 'BUY' then count*price
      when action = 'SELL' then -count*price
     end
     ) as amount,
 max(created_at) as last_trade
from main.trade
group by ticker
order by ticker;
        ''')
        rows = await self.connection.stream(statement)
        async for row in rows:
            obj: PortfolioTicker = PortfolioTicker(
                ticker=row.ticker,
                count=row.count,
                price=row.amount/row.count,
                last_trade=row.last_trade
            )
            yield obj
