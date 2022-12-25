from fastapi import APIRouter
from fastapi.responses import PlainTextResponse


router = APIRouter(tags=['health'])


@router.get(
    '/',
    name='health',
    response_class=PlainTextResponse,
    summary='healthcheck',
)
async def health() -> PlainTextResponse:
    return 'OK'
