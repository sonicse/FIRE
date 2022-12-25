from fastapi import APIRouter

from . import healthcheck

router = APIRouter()
router.add_api_route(
    path='/healthcheck', endpoint=healthcheck.healthcheck, name='healthcheck'
)
