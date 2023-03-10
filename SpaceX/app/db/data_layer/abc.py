from abc import ABC
from typing import Any, ClassVar, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.db.models import TableType

DAOType = TypeVar("DAOType", bound="AbstractDAO")  # pylint: disable =invalid-name


class AbstractDAO(ABC):
    """Abstract base class for Data Access Layer"""

    model: ClassVar[TableType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, item: Any) -> None:
        self.session.add(item)

    def add_all(self, items: list[Any]) -> None:
        self.session.add_all(items)

    async def count(self) -> int | None:
        query = select(func.count(self.model.id))  # pylint: disable=not-callable
        result = await self.session.execute(query)
        return result.scalar()
