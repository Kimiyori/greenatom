from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
)

from app.db.config import get_postgres_uri


async_engine: AsyncEngine = create_async_engine(
    get_postgres_uri(),
    future=True,
    echo=True,
)
Session = async_sessionmaker(async_engine)
