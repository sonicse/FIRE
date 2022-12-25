from fastapi import APIRouter

from . import trade
from . import health


router = APIRouter()
router.include_router(health.router, prefix='/health')
router.include_router(trade.router, prefix='/trades')
