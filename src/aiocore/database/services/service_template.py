from src.aiocore import Database


class DatabaseServiceTemplate:
    __RESERVED_COLUMNS = [
        "id"
    ]

    __TABLE_NAME = ""
    __OBJECT_NAME = ""

    def __init__(self, database: Database):
        """
        To work with the database service in handlers, you need to:
            0. Add import abbreviation to __init__.py (optional)
            1. Import service to src.aiocore.common.core and add it to the constructor of the CoreServices class
            2. Import service to src.aiocore.middlewares.core_middleware and create its object in __call__ method

        Recommendation: do not create objects inside the service constructor.
        Pass them in the middleware following the principles of dependency injection.

        :param database:
        """
        self.__database = database
        self.__connection = self.__database.connection
        self.__cursor = self.__database.cursor

        self.__database.create_table(f""" CREATE TABLE IF NOT EXISTS {self.__TABLE_NAME} (
                                            id              INTEGER     PRIMARY KEY
                                    )""")

    def check_object_exists(self) -> bool:
        return True if self.__cursor.execute(f"SELECT * FROM {self.__TABLE_NAME} WHERE", ()).fetchone() else False

    def get_object_data(self) -> tuple:
        return self.__cursor.execute(f"SELECT * FROM {self.__TABLE_NAME} WHERE", ())

    def add_object(self) -> None:
        self.__cursor.execute(f"INSERT INTO {self.__TABLE_NAME} () VALUES ()", ())
        self.__connection.commit()

    def update_object_data(self) -> None:
        self.__cursor.execute(f"UPDATE {self.__TABLE_NAME} SET", ())
        self.__connection.commit()

    def delete_object(self) -> None:
        self.__cursor.execute(f"DELETE FROM {self.__TABLE_NAME}", ())
        self.__connection.commit()
