from app_etl.etl.etl_interface import ETLInterface
from app_etl.gateway.global_health_data import retrieve_indicator_data
from app_etl.repository.malaria_annual_confirmed_cases_repository import (
    MalariaAnnualConfirmedCasesRepository,
)


class MalariaAnnualConfirmedCasesETL(ETLInterface):
    _indicator_code = "MALARIA_CONF_CASES"
    _keys_mapping = {
        "ParentLocation": "region",
        "ParentLocationCode": "regioncode",
        "SpatialDim": "country",
        "TimeDim": "year",
        "NumericValue": "cases_confirmed",
    }

    def __init__(
        self,
        malariaannualconfirmedcasesrepository: MalariaAnnualConfirmedCasesRepository,
    ) -> None:
        self.malariaannualconfirmedcasesrepository = (
            malariaannualconfirmedcasesrepository
        )

    def name(self):
        return "Malaria Annual Confirmed Cases"

    def extract(self):
        """ """

        """
            TODO:
                handle duplicate data better.
                if we read the same record from the WHO GHO API we should not persist it.
                we should notify the ETL operator via log, slack alert or email.

                possible implementation:
                    1. check wth GHO API if value for "Id" field is unique identifier
                        and create unique constraint on our table's Id column:
                        table: SourceData.WHOGHOMalariaAnnualConfirmedCases
                    2. generate a hash per record:
                        check hash against hashes of already persisted records
                        if match:
                            execute error handling strategy stipulated above
                        else:
                            persist record.
        """
        self.malariaannualconfirmedcasesrepository.save_source_data(
            retrieve_indicator_data(self._indicator_code)
        )

    def retrieve_source_data(self):
        """
        read annual malaria confirmed cases data from local source data store.
        """
        return self.malariaannualconfirmedcasesrepository.retrieve_source_data()

    def transform(self, source_data, etl_id: int):
        """
        objective: maps WHO GHO API fields to our domain definition fields.
        computational complexity analysis:

            mapping fields to domain definition fields:
                N = number of malaria annual confirmed cases
                M = fields per malaria annual confirmed case object = 5

                O(N * M) = O(n * 5) = O(5N) = O(N)

            adding etl_id to each malaria annual confirmed case object
                O(N)

            total computational complexity = O(N) + O(N) = O(2N) = O(N)
            ∴ asymptotic runtime  = O(N)
        """
        """
            TODO:
            - what shoud we do with null values? 
                there are some fields(region) that have nulls:
                - do we exclude the whole record?
                - use an appropriate default?   

            NB: check all of them and decide sensible rules.

            - think about migration checks
                1. same row number saved in target == row number in source

        """
        target_data = [
            {self._keys_mapping.get(key): value for key, value in r.items()}
            for r in source_data
        ]

        for r in target_data:
            r.update(etl_id=etl_id)
        return target_data

    def load(self, data):
        self.malariaannualconfirmedcasesrepository.save_target_data(data)
