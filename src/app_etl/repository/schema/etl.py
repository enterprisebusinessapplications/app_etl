from sqlalchemy import MetaData, Table


class ETL:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.table_store = MetaData(schema="etl")
        self.table_store.reflect(bind=self.engine)

    def etl_table(self) -> Table:
        return self.table_store.tables["etl.etl"]
