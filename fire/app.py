from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fire.conf.settings import settings
from fire.routes import router


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router, prefix=settings.API_PREFIX)
