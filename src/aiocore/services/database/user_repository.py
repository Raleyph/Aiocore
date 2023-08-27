from typing import Union

from src.aiocore.database.database import DatabaseInterface
from src.aiocore.database.ecxeptions import ObjectPresenceException, ReservedParameterError


class UserRepository:
    __RESERVED_COLUMNS = [
        "id",
        "user_id",
        "language",
        "chat_id",
        "state",
        "state_data"
    ]

    __TABLE_NAME = "users"
    __OBJECT_NAME = "user"

    __USER_STATUSES = {
        "user": "USER",
        "admin": "ADMIN"
    }

    def __init__(self, database: DatabaseInterface):
        """
        User storage service

        :param database:
        """
        self.__database = database
        self.__connection = database.connection
        self.__cursor = database.cursor

        self.__database.create_table(f""" CREATE TABLE IF NOT EXISTS {self.__TABLE_NAME} (
                                        id                      INTEGER     PRIMARY KEY,
                                        user_id                 INTEGER     NOT NULL,
                                        username                TEXT,
                                        installed_language      TEXT,
                                        blocked_bot             BOOL        DEFAULT FALSE,
                                        chat_id                 INT,
                                        state                   TEXT,
                                        state_data              TEXT,
                                        status                  TEXT        DEFAULT {self.__USER_STATUSES["user"]}
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
        return True if self.__cursor.execute(f"SELECT * FROM {self.__TABLE_NAME} WHERE user_id = ?",
                                             (user_id,)).fetchone()\
            else False

    def get_all_users(
            self,
            column_name: Union[str, list[str]] = None
    ):
        """
        Return a list of all users or a specific column for all users

        :param column_name:
        :return:
        """
        if not column_name:
            return self.__cursor.execute(f"SELECT * FROM {self.__TABLE_NAME}").fetchall()

        if self.__database.check_column_exists("users", column_name):
            column_query = ", ".join(column_name) if isinstance(column_name, list) else column_name
            return self.__cursor.execute(f"SELECT {column_query} FROM {self.__TABLE_NAME}").fetchall()

    def add_user(
            self,
            user_id: int,
            username: str,
            chat_id: int
    ):
        """
        Add new user to database

        :param user_id:
        :param username:
        :param chat_id:
        :return:
        """
        if not self.check_user_exists(user_id):
            self.__cursor.execute(f"INSERT INTO {self.__TABLE_NAME} (user_id, username, chat_id) "
                                  f"VALUES (?, ?, ?)",
                                  (user_id, username, chat_id))
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
        user_data = self.__cursor.execute(f"SELECT * FROM {self.__TABLE_NAME} WHERE user_id = ?", (user_id,)).fetchone()

        if not user_data:
            raise ObjectPresenceException(self.__TABLE_NAME, self.__OBJECT_NAME, "user_id", user_id)

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
            raise ObjectPresenceException(self.__TABLE_NAME, self.__OBJECT_NAME, "user_id", user_id)

        if self.get_user_data(user_id)[3] is language:
            raise ValueError("Selected language is already set.")

        self.__cursor.execute(f"UPDATE {self.__TABLE_NAME} SET installed_language = ? WHERE user_id = ?",
                              (language, user_id))
        self.__connection.commit()

    def change_user_parameters(self, user_id: int, **parameters):
        if not self.check_user_exists(user_id):
            raise ObjectPresenceException(self.__TABLE_NAME, self.__OBJECT_NAME, "user_id", user_id)

        parameters_name = list(parameters.keys())
        parameters_value = list(parameters.values())

        for parameter in parameters_name:
            if parameter in self.__RESERVED_COLUMNS:
                raise ReservedParameterError(parameter)

        if len(parameters) > 1:
            parameters_execute = " = ?, ".join(parameters_name)
        else:
            parameters_execute = f"{parameters_name[0]} = ?"

        self.__cursor.execute(f"UPDATE {self.__TABLE_NAME} SET {parameters_execute} WHERE user_id = ?",
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
            raise ObjectPresenceException(self.__TABLE_NAME, self.__OBJECT_NAME, "user_id", user_id)

        self.__cursor.execute(f"UPDATE {self.__TABLE_NAME} SET state = ?, state_data = ? WHERE user_id = ?",
                              (state, state_data, user_id))
        self.__connection.commit()
