from src.aiocore.database.database import DatabaseInterface


class DatabaseServiceTemplate:
    __RESERVED_COLUMNS = [
        "id"
    ]

    __TABLE_NAME = ""
    __OBJECT_NAME = ""

    def __init__(self, database: DatabaseInterface):
        """
        To work with the database service in handlers, you need to:
            1. Add import abbreviation to src.aiocore.services.database.__init__.py (optional)
            2. Import service to src.aiocore.core and add it to the constructor of the CoreServices class
            3. Create a service object in the __call__ method of the CoreMiddleware class and pass it to the CoreServices object

        Recommendation: do not create objects inside the service constructor.
        Pass them in the middleware following the principles of dependency injection.

        :param database:
        """
        self.__database = database
        self.__connection = self.__database.__connection
        self.__cursor = self.__database.__cursor

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
