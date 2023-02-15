from dependency_injector import containers, providers
from app.db.data_layer.launch import LaunchDAO
from app.db.data_layer.mission import MissionDAO
from app.db.data_layer.rocket import RocketDAO
from app.db.session import session as db_session


class DatabaseContainer(containers.DeclarativeContainer):
    """Container for dao layer"""

    wiring_config = containers.WiringConfiguration(
        packages=["app.spacex.db_handler", "app.api.endpoints","tests.test_spacex","tests.conftest"]
    )
    session = providers.Resource(db_session)
    rocket = providers.Factory(RocketDAO, session)
    mission = providers.Factory(MissionDAO, session)
    launch = providers.Factory(LaunchDAO, session)
