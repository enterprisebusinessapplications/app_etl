from app_etl.etl.etl_interface import ETLInterface
import logging
from logging import log
from datetime import datetime


class ETLRunner:
    def __init__(self, etls: {str: ETLInterface} = None) -> None:
        self.etls = etls

    def run(self, etl_name: str, etl_id: int):
        etl = self.etls[etl_name]
        log(logging.INFO, f"commencing to run ETL number {etl_id} at {datetime.now()}")
        log(logging.INFO, f"running {etl.name()} ETL")
        log(logging.INFO, "running Extract phase")
        etl.extract()
        log(logging.INFO, "running Transform phase")
        target_data = etl.transform(etl.retrieve_source_data(), etl_id)
        log(logging.INFO, "running Load phase")
        etl.load(target_data)
        log(logging.INFO, f"ETL {etl.name()} completed at {datetime.now()}")

    def batch_run(self, etl_id: int):
        log(logging.INFO, f"commencing to run ETL at {datetime.now()}")
        for etl in self.etls:
            self.run(etl.name(), etl_id)
