from __future__ import annotations
from app.db.models import Launch
from app.db.data_layer.abc import AbstractDAO


class LaunchDAO(AbstractDAO):
    """Data Acess Layer for launch table"""

    model = Launch
