import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from src.api.routers.user_router import router as user_router
from src.api.routers.auth_router import router as auth_router
from src.api.routers.protected_router import router as protected_router
from src.db.repositories.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ТОЛЬКО ДЛЯ УДОБСТВА ТЕСТРОВАНИЯ!"""
    try:
        await init_db()
    except Exception as e:
        raise e
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(protected_router)


if __name__ == "__main__":
    uvicorn.run(app)