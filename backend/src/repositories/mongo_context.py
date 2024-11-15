from typing import TypeVar

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from src.logger import logger
from src.config import db_config
from src.repositories.mongo.base_crud import BaseMongoCRUD

MongoCRUD = TypeVar('MongoCRUD', bound=BaseMongoCRUD)

class MongoContext[MongoCRUD]:
    """ Класс для работы с СУБД MongoDB """

    #: CRUD для взаимодействия с таблицей
    crud: MongoCRUD

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
                 crud: MongoCRUD
                 ):
        if client:
            self.client = client

        self.db: Database = self.client[db_name]

        self.crud = crud
        self.crud.db = self.db
