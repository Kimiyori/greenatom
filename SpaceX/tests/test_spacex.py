from unittest import mock
import pytest
from app.spacex.db_handler import DatabaseConnector
from app.spacex.spacex_queries import LAUNCH_QUERY
from .conftest import db_session_container

MOCK_DATA = {
    "data": {
        "launches": [
            {
                "details": "Engine failure at 33 seconds and loss of vehicle",
                "id": "5eb87cd9ffd86e000604b32a",
                "mission_id": ["5eb87cd9ffd86e000604b32a"],
                "mission_name": "FalconSat",
                "rocket": {
                    "rocket": {
                        "id": "5e9d0d95eda69955f709d1eb",
                        "name": "Falcon 1",
                        "description": "The Falcon 1 was an expendable launch system privately developed and manufactured by SpaceX during 2006-2009. On 28 September 2008, Falcon 1 became the first privately-developed liquid-fuel launch vehicle to go into orbit around the Earth.",
                    }
                },
            },
            {
                "details": "Successful first stage burn and transition to second stage, maximum altitude 289 km, Premature engine shutdown at T+7 min 30 s, Failed to reach orbit, Failed to recover first stage",
                "id": "5eb87cdaffd86e000604b32b",
                "mission_id": ["5eb87cdaffd86e000604b32b"],
                "mission_name": "DemoSat",
                "rocket": {
                    "rocket": {
                        "id": "5e9d0d95eda69955f709d1eb",
                        "name": "Falcon 1",
                        "description": "The Falcon 1 was an expendable launch system privately developed and manufactured by SpaceX during 2006-2009. On 28 September 2008, Falcon 1 became the first privately-developed liquid-fuel launch vehicle to go into orbit around the Earth.",
                    }
                },
            },
        ]
    }
}


@pytest.mark.usefixtures("class_session_factory")
@pytest.mark.asyncio
@mock.patch("app.spacex.spacex_handler.session_context")
async def test_spacex(mock, db_session_container):
    mock.return_value = MOCK_DATA
    db_conn = DatabaseConnector()
    await db_conn.insert_data(LAUNCH_QUERY)
    launches = db_session_container.launch()
    missions = db_session_container.mission()
    rockets = db_session_container.rocket()
    launch_count = await launches.count()
    rocket_count= await rockets.count()
    mission_count=await missions.count()
    assert launch_count == 2
    assert rocket_count == 1 
    assert mission_count == 2
