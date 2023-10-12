import logging
import sys
from logging import log
from datetime import datetime
from flask import Blueprint, Response, request, make_response

from app_etl.etl.malaria_annual_confirmed_cases_etl import (
    MalariaAnnualConfirmedCasesETL,
)
from app_etl.etl.runner import ETLRunner
from app_etl.repository.malaria_annual_confirmed_cases_repository import (
    MalariaAnnualConfirmedCasesRepository,
)

from app_etl.repository.etl_repository import ETLRepository
from app_etl.repository.postgres.connection import PostgresConnection
from app_etl.repository.postgres.postgres_configuration import PostgresConfiguration

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TODO: inject this into container environment on startup when the app is Dockerized
postgres_config = PostgresConfiguration(
    "app_etl", "postgres", "postgres_service", "5432", "app_etl"
)

postgres_connection = PostgresConnection(postgres_config)
malariaannualconfirmedcasesrepository = MalariaAnnualConfirmedCasesRepository(
    postgres_connection
)
malaria_annual_confirmed_cases_etl = MalariaAnnualConfirmedCasesETL(
    malariaannualconfirmedcasesrepository
)

etl_repository = ETLRepository(postgres_connection)
etls = {"Malaria Annual Confirmed Cases": malaria_annual_confirmed_cases_etl}
etl_runner = ETLRunner(etls)

etl_api = Blueprint("etl_api", __name__)


@etl_api.route("/etl/", methods=["POST"])
def start() -> Response:
    """
    starts an ETL for the given etl_name
    create ETL record entry
        return etl_ID
    inject etl_ID into ETL runner
    """
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        etl_key = "etl_name"
        request_data = request.json
        if etl_key not in request_data.keys():
            return "Incorrectly formed request", 422

        etl_id = etl_repository.save_etl(
            {"starttime": datetime.now(), "status": "Started"}
        )
        """
            TODO: make etl_runner.run( async and return immediately after the etl_id afer the ETL object is created.
            usecase: if a frontend or another process triggers an ETL, we wouldn't want it to wait.
            tools:
                celery
                redis/rabbit
        """
        etl_runner.run(request_data[etl_key], etl_id)

        etl_repository.update_etl(
            {
                "id": etl_id,
                "endtime": datetime.now(),
                "status": "Completed",
            }
        )
        return {"etl_id": etl_id}, 201
    else:
        return "Content-Type not supported!"


# @etl_resource.route("/pause")
def pause(etl_id):
    """
    allows pausing an etl
    @param etl_id: int
    """
    pass


# @etl_resource.route("/resume")
def resume(etl_id):
    """
    allows resuming an etl
    @param etl_id: int
    """
    pass


# @etl_resource.route("/retry")
def retry(etl_id):
    """
    allows retrying a failed etl
    @param etl_id: int
    """

    """flow:
        retrieve etl_record
        if etl_record.status is not error
            return 400, "cannot retry an ETL that has not faile"

            execute the etl retry

    """
    pass


# @etl_resource.route("/etls")
def retrieve_etls():
    """
    retrieve all ETLS
    """
    # consider pagination if the number of ETLS is alrge
    pass
