import pytest
import pytest_asyncio
from app.db.data_layer.mission import MissionDAO

from app.db.data_layer.rocket import RocketDAO
from .conftest import dao_session
from app.api.main import create_app
from app.db.container import DatabaseContainer
from app.db.data_layer.launch import LaunchDAO


@pytest_asyncio.fixture
async def app():
    app = await create_app()
    app.container = DatabaseContainer()
    yield app
    app.container.unwire()


@pytest_asyncio.fixture
async def main_app(aiohttp_client, app):
    client = await aiohttp_client(app)
    return client


@pytest.mark.usefixtures("create_data")
@pytest.mark.parametrize("dao", [LaunchDAO])
@pytest.mark.asyncio
async def test_launch_endpoint(main_app, app, dao_session):
    with app.container.launch.override(dao_session):
        resp = await main_app.get("/launch")
        assert resp.status == 200
        text = await resp.json()
        assert text == {"count": 1}


@pytest.mark.usefixtures("create_data")
@pytest.mark.parametrize("dao", [RocketDAO])
@pytest.mark.asyncio
async def test_rocket_endpoint(main_app, app, dao_session):
    with app.container.rocket.override(dao_session):
        resp = await main_app.get("/rocket")
        assert resp.status == 200
        text = await resp.json()
        assert text == {"count": 1}


@pytest.mark.usefixtures("create_data")
@pytest.mark.parametrize("dao", [MissionDAO])
@pytest.mark.asyncio
async def test_mission_endpoint(main_app, app, dao_session):
    with app.container.mission.override(dao_session):
        resp = await main_app.get("/mission")
        assert resp.status == 200
        text = await resp.json()
        assert text == {"count": 1}
