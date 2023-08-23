from abc import ABC, abstractmethod
from typing import Union

import sqlite3
import sys
import os


class DatabaseInterface(ABC):
    @abstractmethod
    def create_table(self, table: str):
        pass

    @abstractmethod
    def check_column_exists(self, table: str, column: str):
        pass


class Database(DatabaseInterface):
    __DATABASE_FILE_PATH = "src/data/database.db"

    def __init__(self):
        """ Database initialization """
        database_file_path = os.path.join(sys.path[1], self.__DATABASE_FILE_PATH)

        if not os.path.exists(database_file_path):
            raise DatabaseFileError()

        self.connection = sqlite3.Connection(database_file_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self, table: str):
        """ Create new table """
        self.connection.execute(table)

    def check_column_exists(
            self,
            table: str,
            columns: Union[str, list[str]]
    ) -> True:
        """
        Return true if current column exist in the table

        :param table:
        :param columns:
        :return:
        """
        for column_data in self.cursor.execute(f"PRAGMA table_info({table})").fetchall():
            if isinstance(columns, str):
                if columns in column_data:
                    return True

            if isinstance(columns, list):
                for column in columns:
                    if column not in column_data:
                        break

                    return True

        raise ColumnExistsError(table, columns)


# Exceptions

class DatabaseFileError(Exception):
    def __init__(self):
        """ Raise when the database file path does not exist in the main project directory """
        pass

    def __str__(self):
        return "The database file does not exists in main project directory."


class ColumnExistsError(Exception):
    def __init__(self, table: str, column: str):
        """ Raise when the table does not exist current column"""
        self.table = table
        self.column = column

    def __str__(self):
        return f"The table \"{self.table}\" does not exist column \"{self.column}\"."
