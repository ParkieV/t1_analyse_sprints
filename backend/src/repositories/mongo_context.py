from pymongo import MongoClient
from pymongo.database import Database

from src.config import db_config
from src.repositories.mongo.base_crud import BaseMongoCRUD



class MongoContext:
    """ Класс для работы с СУБД MongoDB """

    #: CRUD для взаимодействия с таблицей
    crud: BaseMongoCRUD

    #: Клиент СУБД
    client: MongoClient

    #: База данных
    db: Database

    def __init__(self, *,
                 client: MongoClient = MongoClient(db_config.db_url),
                 db_name: str = db_config.db_name,
                 collection_name: str):
        self.client = client
        self.db: Database = client[db_name]
        self.crud = BaseMongoCRUD(self.db, collection_name)
