import logging

from typing import List, Optional, Any
from advanced_database_replace.database import Database
from advanced_database_replace.database_credentials import DatabaseCredentials
from advanced_database_replace.replacer import Replacer

logr = logging.getLogger(__name__)


class DatabaseReplace:
    def __init__(self, credentials: DatabaseCredentials, serializer: Optional[Any] = None):
        self.__credentials = credentials
        self.__database = Database(self.__credentials)
        self.__replacer = Replacer(serializer=serializer)

    def get_tables(self) -> List[str]:
        res = self.__database.query('SHOW TABLES;')
        res = [list(r.values())[0] for r in res]
        return res

    def describe_table(self, table: str):
        res = self.__database.query(f'DESCRIBE {table};')
        return res

    def get_primary_key(self, table: str) -> str:
        description = self.describe_table(table)
        description = [d for d in description if d['Key'] == 'PRI']
        description = description[0]
        return description['Field']

    def get_records(self, table: str):
        res = self.__database.query(f'SELECT * FROM {table};')
        return res

    def replace(self, old: str, new: str, table: str):
        primary_key_name = self.get_primary_key(table)
        logr.info(f'Primary key name of {table} table is: {primary_key_name}.')

        logr.info(f'Fetching {table} table records...')
        records = self.get_records(table)

        changed_records: int = 0

        logr.info(f'Running find&replace on {table} table records...')
        for record in records:
            for key, value in record.items():
                primary_key_value = record[primary_key_name]

                original_value = value
                new_value = self.__replacer.replace(original_value, old, new)

                if original_value != new_value:
                    logr.info(f'Updating "{original_value[:50]}..." with new "{new_value[:50]}..."...')
                    self.__database.query(f'UPDATE {table} SET {key}=%s WHERE {primary_key_name}=%s;', (new_value, primary_key_value))
                    changed_records += 1

        logr.info(f'Total changed records: {changed_records}.')

    def replace_all(self, old: str, new: str):
        tables = self.get_tables()

        for table in tables:
            self.replace(old, new, table)
