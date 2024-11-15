from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from src.config import db_config
from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD



class MongoContext:
    """ Класс для работы с СУБД MongoDB """

    #: CRUD для взаимодействия с таблицей
    crud: BaseMongoCRUD

    #: Клиент СУБД
    client: MongoClient = MongoClient(db_config.db_url)

    #: База данных
    db: Database

    @classmethod
    def check_connection(cls):
        logger.info("Try to connect to MongoDB")
        try:
            cls.client.admin.command('ping')
            logger.info("Connection to MongoDB is successful!")
        except Exception as e:
            logger.error(f"Connection to MongoDB failed: {e.__class__.__name__} - {e}")
            raise ConnectionFailure("Connection to MongoDB failed!")

    def __init__(self, *,
                 client: MongoClient | None = None,
                 db_name: str = db_config.db_name,
                 collection_name: str):
        if client:
            self.client = client
        self.db: Database = self.client[db_name]
        self.crud = BaseMongoCRUD(self.db, collection_name)
