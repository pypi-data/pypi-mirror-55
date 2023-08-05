import pymysql

from typing import Any, Dict, Optional
from advanced_database_replace.database_credentials import DatabaseCredentials


class Database:
    def __init__(self, credentials: DatabaseCredentials):
        self.__credentials = credentials

    def __get_connection(self) -> pymysql.Connection:
        return pymysql.connect(
            host=self.__credentials.host,
            user=self.__credentials.username,
            password=self.__credentials.password,
            db=self.__credentials.database_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def query(self, query: str, args: Optional[tuple] = None) -> Dict[Any, Any]:
        connection = self.__get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, args or tuple())
                result = cursor.fetchall()
                connection.commit()
                return result
        finally:
            connection.close()
