import logging
from logging import log

from sqlalchemy import insert, update

from app_etl.repository.postgres.connection import PostgresConnection
from app_etl.repository.schema.etl import ETL


class ETLRepository:
    def __init__(self, database_connection: PostgresConnection) -> None:
        self.database_connection = database_connection
        self.source_schema = ETL(database_connection.get_connection_engine())

    def save_etl(self, data) -> int:
        with self.database_connection.get_connection() as conn:
            result = conn.execute(
                insert(self.source_schema.etl_table()).returning(
                    self.source_schema.etl_table().c.id,
                    self.source_schema.etl_table().c.starttime,
                    self.source_schema.etl_table().c.endtime,
                    self.source_schema.etl_table().c.status,
                ),
                data,
            )
            conn.commit()
            log(logging.INFO, f"successfully saved {result.rowcount}")
            return result.mappings().one()["id"]

    def update_etl(self, data):
        with self.database_connection.get_connection() as conn:
            table = self.source_schema.etl_table()
            result = conn.execute(
                update(table)
                .where(table.c.id == data["id"])
                .values(
                    endtime=data["endtime"],
                    status=data["status"],
                )
            )
            conn.commit()
            log(logging.INFO, f"successfully saved {result.rowcount}")

    def retrieve_etl(self, etl_id):
        pass
