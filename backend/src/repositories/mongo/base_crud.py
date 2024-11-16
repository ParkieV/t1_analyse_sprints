from abc import abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any, TypeVar

from attrs import define
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.logger import logger
from src.schemas.user import CustomBaseModel


SchemaOut = TypeVar("SchemaOut", bound=CustomBaseModel)

@define
class BaseMongoCRUD:
    """ Базовый класс для работы с коллекциями MongoDB """

    collection_name: str
    db: AsyncIOMotorDatabase | None = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if self.db is None:
            raise ValueError("Database is empty")
        else:
            return self.db[self.collection_name]

    async def _get_object_by_id(self, object_id: str) -> Mapping[str, Any]:
        try:
            mongo_object = await self.collection.find_one({'_id': ObjectId(object_id)})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise

        return mongo_object

    @abstractmethod
    async def get_object_by_id(self, *args, **kwargs) -> Any:
        pass

    async def _get_objects(self, out_schema: type(SchemaOut), offset: int | None = None, limit: int | None = None) -> list[Mapping[str, Any]]:
        try:
            objects = self.collection.find()
            if offset is not None:
                objects = objects.skip(offset)
            if limit is not None:
                objects = objects.limit(limit)
        except Exception as e:
            logger.error(f"Failed to find objects. {e.__class__.__name__}: {e}", )
            raise

        return [out_schema(**db_object) for db_object in await objects.to_list()]

    @abstractmethod
    async def get_objects(self, *args, **kwargs) -> Any:
        pass

    async def insert_objects(self, data: Sequence[Mapping[str, Any]]) -> None:
        try:
            await self.collection.insert_many(data)
        except Exception as e:
            logger.error(f"Failed to insert objects. {e.__class__.__name__}: {e}", )
            raise