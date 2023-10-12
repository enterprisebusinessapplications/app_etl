import abc

"""
    an interface that any ETL  must comply with.
    this ensures pattern consistency.
"""


class ETLInterface(metaclass=abc.ABCMeta):
    def __init__(self, database_connection) -> None:
        self.database_connection = database_connection

    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def extract(self):
        """
        read data from source system
        and persist in source data store.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_source_data(self):
        """
        read data from local source data store
        hint: read only the fields required in the target data set.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def transform(self, source_data, etl_id: int):
        """
        apply validations and transformations.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, data):
        """
        save data into target data store.
        """
        raise NotImplementedError
