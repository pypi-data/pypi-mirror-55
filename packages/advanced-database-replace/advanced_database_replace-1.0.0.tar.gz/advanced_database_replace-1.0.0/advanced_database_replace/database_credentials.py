from typing import Optional


class DatabaseCredentials:
    def __init__(
            self,
            username: Optional[str] = None,
            password: Optional[str] = None,
            database_name: Optional[str] = None,
            host: Optional[str] = None,
            port: Optional[str] = None
    ):
        self.username = username
        self.password = password
        self.database_name = database_name
        self.host = host
        self.port = port
