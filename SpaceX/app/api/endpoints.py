import json
from aiohttp import web
from dependency_injector.wiring import Provide, inject, Closing

from app.db.data_layer.launch import LaunchDAO
from app.db.data_layer.mission import MissionDAO
from app.db.data_layer.rocket import RocketDAO
from app.db.container import DatabaseContainer


@inject
async def launch_view(
    request: web.Request,  # pylint: disable=unused-argument
    data_layer: LaunchDAO = Closing[Provide[DatabaseContainer.launch]],
) -> web.Response:
    data = await data_layer.count()
    return web.Response(
        text=json.dumps({"count": data}), content_type="application/json"
    )


@inject
async def rocket_view(
    request: web.Request,  # pylint: disable=unused-argument
    data_layer: RocketDAO = Closing[Provide[DatabaseContainer.rocket]],
) -> web.Response:
    data = await data_layer.count()
    return web.Response(
        text=json.dumps({"count": data}), content_type="application/json"
    )


@inject
async def mission_view(
    request: web.Request,  # pylint: disable=unused-argument
    data_layer: MissionDAO = Closing[Provide[DatabaseContainer.mission]],
) -> web.Response:
    data = await data_layer.count()
    return web.Response(
        text=json.dumps({"count": data}), content_type="application/json"
    )
