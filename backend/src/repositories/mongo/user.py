from pymongo.database import Database

from src.repositories.mongo.base_crud import BaseMongoCRUD


class UserCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'user' """

    def __init__(self, db: Database, collection_name: str = "users"):
        super().__init__(db, collection_name)