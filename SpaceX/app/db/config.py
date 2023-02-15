import environs


TEST_DATABASE_NAME = "test_db"


def get_postgres_uri(database_name: bool = True, test: bool = False) -> str:
    env = environs.Env()
    env.read_env(".env")
    host = env("POSTGRES_HOST")
    port = env("POSTGRES_PORT")
    password = env("POSTGRES_PASSWORD")
    user = env("POSTGRES_USER")
    db_name = (
        (env("POSTGRES_NAME") if not test else TEST_DATABASE_NAME)
        if database_name
        else None
    )

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name if db_name else ''}"
