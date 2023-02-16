from __future__ import annotations
from sqlalchemy import select

from app.db.models import Rocket
from app.db.data_layer.abc import AbstractDAO


class RocketDAO(AbstractDAO):
    """Data Acess Layer for rocket table"""

    model = Rocket

    async def get(self, model_id: str) -> Rocket | None:
        query = select(self.model).where(self.model.id == model_id)
        result = await self.session.execute(query)
        return result.scalar()
