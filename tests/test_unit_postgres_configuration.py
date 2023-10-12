from app_etl.repository.postgres.postgres_configuration import PostgresConfiguration
import uuid


def test_correctly_generate_uri():
    username = uuid.uuid4()
    password = uuid.uuid4()
    host = uuid.uuid4()
    port = uuid.uuid4()
    database_name = uuid.uuid4()
    config = PostgresConfiguration(username, password, host, port, database_name)

    excepted_uri = (
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
    )
    assert excepted_uri == config.uri()
