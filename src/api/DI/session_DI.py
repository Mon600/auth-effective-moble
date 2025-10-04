from typing import AsyncGenerator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import async_session


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e

SessionDep = Annotated[AsyncSession, Depends(get_session)]