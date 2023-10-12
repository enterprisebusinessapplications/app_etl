import logging
from logging import log

from sqlalchemy import insert, select

from app_etl.repository.postgres.connection import PostgresConnection
from app_etl.repository.schema.malaria import Malaria
from app_etl.repository.schema.source_data import SourceData


class MalariaAnnualConfirmedCasesRepository:
    def __init__(self, database_connection: PostgresConnection) -> None:
        self.database_connection = database_connection
        self.source_schema = SourceData(database_connection.get_connection_engine())
        self.target_schema = Malaria(database_connection.get_connection_engine())

    def save_source_data(self, data) -> None:
        with self.database_connection.get_connection() as conn:
            result = conn.execute(
                insert(
                    self.source_schema.who_gho_malaria_annual_confirmed_cases_table()
                ),
                data,
            )
            conn.commit()

            log(logging.INFO, f"successfully saved {result.rowcount}")

    def retrieve_source_data(self):
        table_columns = (
            self.source_schema.who_gho_malaria_annual_confirmed_cases_table().c
        )
        with self.database_connection.get_connection() as conn:
            result = conn.execute(
                select(
                    table_columns.ParentLocation,
                    table_columns.ParentLocationCode,
                    table_columns.SpatialDim,
                    table_columns.TimeDim,
                    table_columns.NumericValue,
                )
            )
            return result.mappings().all()

    def save_target_data(self, data) -> None:
        with self.database_connection.get_connection() as conn:
            result = conn.execute(
                insert(self.target_schema.annual_confirmed_cases_table()),
                data,
            )
            conn.commit()

            log(logging.INFO, f"successfully saved {result.rowcount}")
