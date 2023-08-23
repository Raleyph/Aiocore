from typing import Union

from src.aiocore import Database


class UserStorage:
    __RESERVED_COLUMNS = [
        "id",
        "user_id",
        "language",
        "chat_id",
        "state",
        "state_data"
    ]

    def __init__(self, database: Database):
        """
        User storage service

        :param database:
        """
        self.__database = database
        self.__connection = database.connection
        self.__cursor = database.cursor

        self.__database.create_table(""" CREATE TABLE IF NOT EXISTS users (
                                        id                      INTEGER     PRIMARY KEY,
                                        user_id                 INTEGER     NOT NULL,
                                        username                TEXT,
                                        installed_language      TEXT,
                                        blocked_bot             BOOL        DEFAULT FALSE,
                                        chat_id                 INT,
                                        state                   TEXT,
                                        state_data              TEXT
                                    ) """)

    def check_user_exists(
            self,
            user_id: int
    ) -> bool:
        """
        Check id in users table

        :param user_id:
        :return:
        """
        return True if self.__cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()\
            else False

    def get_all_users(
            self,
            column_name: Union[str, list[str]] = None
    ):
        """

        :param column_name:
        :return:
        """
        if not column_name:
            return self.__cursor.execute("SELECT * FROM users").fetchall()

        if self.__database.check_column_exists("users", column_name):
            column_query = ", ".join(column_name) if isinstance(column_name, list) else column_name
            return self.__cursor.execute(f"SELECT {column_query} FROM users").fetchall()

    def add_user(
            self,
            user_id: int,
            username: str,
            language: str,
            chat_id: int
    ):
        """
        Add new user to database

        :param user_id:
        :param username:
        :param language:
        :param chat_id:
        :return:
        """
        if not self.check_user_exists(user_id):
            self.__cursor.execute("INSERT INTO users (user_id, username, installed_language, chat_id) "
                                  "VALUES (?, ?, ?, ?)",
                                  (user_id, username, language, chat_id))
            self.__connection.commit()

    def get_user_data(
            self,
            user_id: int
    ) -> tuple:
        """
        Return all user data from id

        :param user_id:
        :return:
        """
        user_data = self.__cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

        if not user_data:
            raise UserPresenceException(user_id)

        return user_data

    def change_user_language(
            self,
            user_id: int,
            language: str
    ):
        """
        Change installed language

        :param user_id:
        :param language:
        :return:
        """
        if not self.check_user_exists(user_id):
            raise UserPresenceException(user_id)

        if self.get_user_data(user_id)[3] is language:
            raise ValueError("Selected language is already set.")

        self.__cursor.execute("UPDATE users installed_language = ? WHERE user_id = ?", (language, user_id))
        self.__connection.commit()

    def change_user_parameters(self, user_id: int, **parameters):
        if not self.check_user_exists(user_id):
            raise UserPresenceException(user_id)

        parameters_name = list(parameters.keys())
        parameters_value = list(parameters.values())

        for parameter in parameters_name:
            if parameter in self.__RESERVED_COLUMNS:
                raise ReservedParameterError(parameter)

        if len(parameters) > 1:
            parameters_execute = " = ?, ".join(parameters_name)
        else:
            parameters_execute = f"{parameters_name[0]} = ?"

        self.__cursor.execute(f"UPDATE users SET {parameters_execute} WHERE user_id = ?",
                              (*parameters_value, user_id))
        self.__connection.commit()

    def save_user_state(
            self,
            user_id: int,
            state: str,
            state_data: dict
    ):
        """
        Save user state and state data

        :param user_id:
        :param state:
        :param state_data:
        :return:
        """
        if not self.check_user_exists(user_id):
            raise UserPresenceException(user_id)

        self.__cursor.execute("UPDATE users SET state = ?, state_data = ? WHERE user_id = ?",
                              (state, state_data, user_id))
        self.__connection.commit()


# Exceptions

class UserPresenceException(Exception):
    def __init__(self, user_id: int):
        """
        Raise when the user is not in the database

        :param user_id:
        :return:
        """
        self.user_id = user_id

    def __str__(self):
        return f"The required user was not found in the database.\n" \
               f"User ID: {self.user_id}"


class ReservedParameterError(Exception):
    def __init__(self, parameter: str):
        """
        Raise when trying to change a reserved parameter

        :param parameter:
        """
        self.parameter = parameter

    def __str__(self):
        return f"Cannot change reserved parameter {self.parameter} in user storage."
