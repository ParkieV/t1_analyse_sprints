from uuid import UUID

from attrs import define
from pymongo.database import Database
from pymongo.collection import Collection

from src.logger import logger

@define
class BaseMongoCRUD:
    """ Базовый класс для работы с коллекциями MongoDB """

    collection_name: str
    db: Database | None = None

    @property
    def collection(self):
        if self.db is None:
            raise ValueError("Database is empty")
        else:
            return self.db[self.collection_name]

    async def get_object_by_id(self, object_id: UUID):
        try:
            user = self.collection.find_one({'_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find user by id. {e.__class__.__name__}: {e}", )
            raise e

        return user