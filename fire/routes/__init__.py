from fastapi import APIRouter

from . import trade
from . import health
from . import portfolio


router = APIRouter()
router.include_router(health.router, prefix='/health')
router.include_router(trade.router, prefix='/trades')
router.include_router(portfolio.router, prefix='/portfolio')
