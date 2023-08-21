import sqlite3
import sys
import os


class Database(object):
    __DATABASE_FILE_PATH = "src/data/database.db"

    def __init__(self):
        """ Database initialization """
        database_file_path = os.path.join(sys.path[1], self.__DATABASE_FILE_PATH)

        if not os.path.exists(database_file_path):
            raise DatabaseFileError()

        self.connection = sqlite3.Connection(database_file_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """ Create new tables """

        # create users table
        self.connection.execute((""" CREATE TABLE IF NOT EXISTS users (
                                id                      INTEGER     PRIMARY KEY,
                                user_id                 INTEGER     NOT NULL,
                                username                TEXT,
                                installed_language      TEXT,
                                blocked_bot             BOOL        DEFAULT FALSE
                            ) """))

    # Users

    def check_user_exists_in_database(
            self,
            user_id: int
    ) -> bool:
        """
        Check id in users table

        :param user_id:
        :return:
        """
        return True if self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()\
            else False

    def get_user_data(
            self,
            user_id: int
    ) -> tuple:
        """
        Return all user data from id

        :param user_id:
        :return:
        """
        user_data = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

        if not user_data:
            raise UserPresenceException(user_id)

        return user_data

    def add_user_to_database(
            self,
            user_id: int,
            username: str,
            language: str
    ):
        """
        Add new user to database

        :param user_id:
        :param username:
        :param language:
        :return:
        """
        if not self.check_user_exists_in_database(user_id):
            self.cursor.execute("INSERT INTO users (user_id, username, installed_language) VALUES (?, ?, ?)",
                                (user_id, username, language))
            self.connection.commit()

    def change_installed_user_language(
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
        if self.get_user_data(user_id)[3] is language:
            raise sqlite3.Error("Selected language is already set.")

        self.cursor.execute("UPDATE users installed_language = ? WHERE user_id = ?", (language, user_id))
        self.connection.commit()


# Exceptions

class DatabaseFileError(Exception):
    def __init__(self):
        """ Raise when the database file path does not exist in the main project directory """
        pass

    def __str__(self):
        return "The database file does not exists in main project directory."


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
