from fastapi import FastAPI
from app.api.routers import auth
from app.core.cache import init_cache

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth")


@app.on_event("startup")
async def on_startup():
    init_cache()