import logging
from aiohttp import web
from app.api.routes import setup_routes
from app.db.container import DatabaseContainer
from app.spacex.db_handler import DatabaseConnector
from app.spacex.spacex_queries import LAUNCH_QUERY


async def create_app() -> web.Application:
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    setup_routes(app)
    return app


async def populate_db() -> None:
    db_conn = DatabaseConnector()
    await db_conn.insert_data(LAUNCH_QUERY)


async def main() -> web.Application:
    DatabaseContainer()
    await populate_db()
    app = await create_app()
    return app
