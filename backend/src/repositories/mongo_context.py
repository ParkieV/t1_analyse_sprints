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
    _crud: MongoCRUD | None = None

    #: Клиент СУБД
    client: MongoClient = MongoClient(db_config.db_url)

    #: База данных
    db: Database

    @property
    def crud(self) -> MongoCRUD:
        if self._crud:
            return self._crud
        else:
            raise ValueError('CRUD object has not been initialized')

    @crud.setter
    def crud(self, crud: MongoCRUD):
        self._crud = crud
        self._crud.db = self.db

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
                 crud: MongoCRUD | None = None,
                 ):
        if client:
            self.client = client

        self.db: Database = self.client[db_name]

        if crud:
            self._crud = crud
            self._crud.db = self.db
