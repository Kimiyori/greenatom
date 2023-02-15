from typing import AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.data_layer.abc import DAOType
from app.db.base import Session


async def session(
    model: Callable[[AsyncSession], DAOType] | None = None
) -> AsyncGenerator[DAOType, None] | AsyncSession:
    async with Session() as session_con:
        yield model(session_con) if model else session_con
