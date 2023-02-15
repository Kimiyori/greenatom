from __future__ import annotations
from typing import TypedDict
from dependency_injector.wiring import Provide, inject, Closing
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.data_layer.mission import MissionDAO
from app.db.data_layer.rocket import RocketDAO
from app.db.data_layer.launch import LaunchDAO
from app.db.models import Launch, Mission, Rocket
from app.spacex.spacex_handler import get_data
from app.db.container import DatabaseContainer


class RocketData(TypedDict):
    """TypedDict for rocket data"""

    id: str
    name: str | None
    description: str | None


class LaunchData(TypedDict):
    """TypedDict for launch data"""

    id: str
    details: str | None
    mission_id: list[str]
    mission_name: str | None
    rocket: dict[str, RocketData]


class DatabaseConnector:
    """
    Class for handling scraped data and insert it into db
    """

    @staticmethod
    @inject
    async def check_count(
        launch_session: LaunchDAO = Provide[DatabaseContainer.launch],
    ) -> bool:
        data = await launch_session.count()
        return not data

    @inject
    async def handle_launch_data(
        self,
        data: LaunchData,
        launch_session: LaunchDAO = Provide[DatabaseContainer.launch],
    ) -> None:
        launch = Launch(id=data["id"], details=data["details"])
        await self.handle_mission_data(
            data["mission_id"][0], data["mission_name"], launch
        )
        await self.handle_rocket_data(data["rocket"]["rocket"], launch)
        launch_session.add(launch)

    @staticmethod
    @inject
    async def handle_mission_data(
        mission_id: str,
        mission_name: str | None,
        launch: Launch,
        mission_session: MissionDAO = Provide[DatabaseContainer.mission],
    ) -> None:
        mission = Mission(id=mission_id, name=mission_name, launch=launch)
        mission_session.add(mission)

    @staticmethod
    @inject
    async def handle_rocket_data(
        rocket_data: RocketData,
        launch: Launch,
        rocket_session: RocketDAO = Provide[DatabaseContainer.rocket],
    ) -> None:
        rocket_id = rocket_data["id"]
        rocket = await rocket_session.get(rocket_id)
        if not rocket:
            rocket = Rocket(
                id=rocket_id,
                description=rocket_data["description"],
                name=rocket_data["name"],
                launch=launch,
            )
            rocket_session.add(rocket)

    @inject
    async def insert_data(
        self,
        query: str,
        session: AsyncSession = Closing[Provide[DatabaseContainer.session]],
    ) -> None:
        empty_db = await self.check_count()
        if empty_db:
            data = await get_data(query)
            for item in data["data"]["launches"]:
                await self.handle_launch_data(item)
            await session.commit()
