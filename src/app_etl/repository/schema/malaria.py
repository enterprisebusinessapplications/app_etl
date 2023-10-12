from sqlalchemy import MetaData, Table


class Malaria:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.table_store = MetaData(schema="malaria")
        self.table_store.reflect(bind=self.engine)

    def annual_confirmed_cases_table(self) -> Table:
        return self.table_store.tables["malaria.annualconfirmedcases"]
