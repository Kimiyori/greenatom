import asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import pytest
import pytest_asyncio
from sqlalchemy import text
from app.db.config import TEST_DATABASE_NAME, get_postgres_uri
from app.db.container import DatabaseContainer
from app.db.models import Base, Launch, Mission, Rocket


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def test_engine():
    engine_aux = create_async_engine(
        get_postgres_uri(database_name=False),
        future=True,
    )
    await create_db(engine_aux)
    engine = create_async_engine(
        get_postgres_uri(test=True),
        future=True,
        echo=False,
    )
    try:
        yield engine
    finally:
        await drop_db(engine_aux)


@pytest_asyncio.fixture(scope="module")
async def class_session_factory(test_engine):
    await create_tables(test_engine)
    try:
        yield async_sessionmaker(test_engine, expire_on_commit=False)
    finally:
        await drop_tables(test_engine)


@pytest_asyncio.fixture
async def session_factory(test_engine):
    yield async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def session(
    session_factory,
):
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def db_session_container(session):
    container = DatabaseContainer()
    container.session.override(session)
    yield container
    container.unwire()


@pytest_asyncio.fixture
async def dao_session(session_factory, dao):
    async with session_factory() as session:
        yield dao(session) if dao else session


async def create_db(engine) -> None:
    async with engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        try:
            await conn.execute(text(f"create database {TEST_DATABASE_NAME}"))
        except sqlalchemy.exc.ProgrammingError:
            await conn.execute(
                text(f"drop database if exists {TEST_DATABASE_NAME} WITH (FORCE)")
            )
            await conn.execute(text(f"create database {TEST_DATABASE_NAME}"))


async def create_tables(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def drop_db(engine) -> None:
    async with engine.connect() as conn:
        await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(
            text(f"drop database if exists {TEST_DATABASE_NAME} WITH (FORCE)")
        )
        await engine.dispose()


@pytest_asyncio.fixture(scope="module")
async def create_data(class_session_factory) -> None:
    async with class_session_factory() as session:
        pytest.launch = Launch(
            id="5eb87cd9ffd86e000604b32a",
            details="Engine failure at 33 seconds and loss of vehicle",
        )
        pytest.rocket = Rocket(
            id="5e9d0d95eda69955f709d1eb",
            name="Falcon 1",
            description=(
                "The Falcon 1 was an expendable launch system privately developed and manufactured "
                "by SpaceX during 2006-2009. On 28 September 2008, Falcon 1 became "
                "the first privately-developed liquid-fuel launch "
                "vehicle to go into orbit around the Earth."
            ),
            launch=pytest.launch,
        )
        pytest.mission = Mission(
            id="5eb87cdaffd86e000604b32b", name="DemoSat", launch=pytest.launch
        )
        session.add(pytest.launch)
        session.add(pytest.rocket)
        session.add(pytest.mission)
        await session.commit()
