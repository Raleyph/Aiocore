from typing import Union


class DatabaseFileError(Exception):
    def __init__(self):
        """ Raise when the database file path does not exist in the main project directory """
        pass

    def __str__(self):
        return "The database file does not exists in main project directory."


class ColumnExistsError(Exception):
    def __init__(self, table: str, column: str):
        """
        Raise when the table does not exist current column

        :param table:
        :param column:
        """
        self.table = table
        self.column = column

    def __str__(self):
        return f"The table \"{self.table}\" does not exist column \"{self.column}\"."


class ObjectPresenceException(Exception):
    def __init__(
            self,
            table: str,
            object_name: str,
            filter_parameter_name: str,
            filter_parameter: Union[int, str]
    ):
        """
        Raise when the object is not in the database

        :param table:
        :param object_name:
        :param filter_parameter_name:
        :param filter_parameter:
        """
        self.table = table
        self.object_name = object_name
        self.filter_parameter_name = filter_parameter_name
        self.filter_parameter = filter_parameter

    def __str__(self):
        return f"The required object \"{self.object_name}\" with " \
               f"\"{self.filter_parameter_name}\" = \"{self.filter_parameter}\" " \
               f"was not found in the \"{self.table}\" table.\n"


class ReservedParameterError(Exception):
    def __init__(self, parameter: str):
        """
        Raise when trying to change a reserved parameter

        :param parameter:
        """
        self.parameter = parameter

    def __str__(self):
        return f"Cannot change reserved parameter {self.parameter} in user storage."

