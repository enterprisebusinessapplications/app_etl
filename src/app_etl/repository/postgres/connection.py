from sqlalchemy import create_engine
from repository.postgres.postgres_configuration import PostgresConfiguration
from sqlalchemy.engine import Engine, Connection


class PostgresConnection:
    def __init__(self, postgres_config: PostgresConfiguration) -> None:
        # TODO: switch off echo=True for PROD.
        # for full PROD implementation app make this configurable. True in DEV and false in PROD
        self.engine = create_engine(postgres_config.uri())

    def get_connection(self) -> Connection:
        return self.engine.connect()

    def get_connection_engine(self) -> Engine:
        return self.engine
