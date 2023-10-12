from sqlalchemy import MetaData, Table


class SourceData:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.table_store = MetaData(schema="sourcedata")
        self.table_store.reflect(bind=self.engine)

    def who_gho_malaria_annual_confirmed_cases_table(self) -> Table:
        return self.table_store.tables["sourcedata.whoghomalariaannualconfirmedcases"]
