from __future__ import annotations
from app.db.models import Mission

from app.db.data_layer.abc import AbstractDAO


class MissionDAO(AbstractDAO):
    """Data Acess Layer for mission table"""

    model = Mission
