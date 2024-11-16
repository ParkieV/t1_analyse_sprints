from collections.abc import Callable, Coroutine
from typing import TypeVar, ParamSpec, Mapping, Any

from attrs import define
from bson import ObjectId

from src.logger import logger
from src.schemas.data import SprintOutDTO
from src.repositories.mongo.base_crud import BaseMongoCRUD, SchemaOut
from src.schemas.user import CustomBaseModel

T = TypeVar("T", bound=CustomBaseModel)
P = ParamSpec("P")
AsyncFunc = Callable[P, Coroutine[None, None, T]]

@define
class SprintsCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'sprints' """

    collection_name: str = 'sprints'

    async def get_objects(self, out_schema: type(SchemaOut), offset: int | None = None, limit: int | None = None) -> list[Mapping[str, Any]]:
        return await self._get_objects(out_schema, offset, limit)

    async def get_object_by_id(self, object_id: ObjectId) -> dict:
        logger.info('Start finding sprint')
        try:
            sprint = await self.collection.find_one({'_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise
        logger.info('Sprint found successfully')
        return sprint