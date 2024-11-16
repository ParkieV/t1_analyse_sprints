from collections.abc import Callable, Coroutine
from typing import TypeVar, ParamSpec

from attrs import define
from bson import ObjectId

from src.logger import logger
from src.schemas.data import SprintOutDTO
from src.repositories.mongo.base_crud import BaseMongoCRUD
from src.schemas.user import CustomBaseModel

T = TypeVar("T", bound=CustomBaseModel)
P = ParamSpec("P")
AsyncFunc = Callable[P, Coroutine[None, None, T]]

@define
class SprintsCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'sprints' """

    collection_name: str = 'sprints'

    async def get_object_by_id(self, object_id: ObjectId, entity_getting_func: AsyncFunc) -> SprintOutDTO:
        logger.info('Start finding sprint')
        try:
            sprint = self.collection.find_one({'_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise
        logger.info('Sprint found successfully')

        logger.info('Started preparing sprint model')
        if entities := sprint.get('entity_ids'):
            sprint['entity_ids'] = [await entity_getting_func(entity) for entity in entities]
        logger.info('Sprint model prepared successfully')
        return SprintOutDTO(**sprint)