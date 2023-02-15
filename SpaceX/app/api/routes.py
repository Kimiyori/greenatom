from aiohttp.web import Application
from app.api.endpoints import launch_view, rocket_view, mission_view


def setup_routes(app: Application) -> None:
    app.router.add_get("/launch", launch_view, name="launch_count")
    app.router.add_get("/mission", mission_view, name="mission_count")
    app.router.add_get("/rocket", rocket_view, name="rocket_count")
