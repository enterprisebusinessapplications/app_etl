class PostgresConfiguration:
    def __init__(self, username, password, host, port, database_name) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

    def uri(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}"
