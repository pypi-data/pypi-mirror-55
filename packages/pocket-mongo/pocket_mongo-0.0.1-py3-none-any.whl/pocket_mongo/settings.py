class Settings:
    address: str = None
    database: str = None

    @classmethod
    def config(cls, mongo_address, mongo_db) -> None:
        """
        Set the connection string and default database for the MongoDb
        instance.

        :param mongo_address: Connection string to MongoDb
        :param mongo_db: Default database
        :return:
        """
        cls.database = mongo_db
        cls.address = mongo_address
