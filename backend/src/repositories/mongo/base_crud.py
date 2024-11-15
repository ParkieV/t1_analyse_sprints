from collections.abc import Mapping, Sequence
from typing import Any
from uuid import UUID

from attrs import define
from pymongo.database import Database

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

    async def get_object_by_id(self, object_id: UUID) -> Mapping[str, Any]:
        try:
            mongo_object = self.collection.find_one({'_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise

        return mongo_object

    async def get_objects(self, offset: int | None = None, limit: int | None = None) -> list[Mapping[str, Any]]:
        try:
            objects = self.collection.find()
            if offset is not None:
                objects = objects.skip(offset)
            if limit is not None:
                objects = objects.limit(limit)
        except Exception as e:
            logger.error(f"Failed to find objects. {e.__class__.__name__}: {e}", )
            raise

        return objects.to_list()

    async def insert_objects(self, data: Sequence[Mapping[str, Any]]) -> None:
        try:
            self.collection.insert_many(data)
        except Exception as e:
            logger.error(f"Failed to insert objects. {e.__class__.__name__}: {e}", )
            raise