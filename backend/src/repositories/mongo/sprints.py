from collections.abc import Callable, Coroutine
from typing import TypeVar, ParamSpec, Any, Sequence

from attrs import define
from bson import ObjectId

from src.logger import logger
from src.repositories.mongo.entities import EntitiesCRUD
from src.repositories.mongo_context import MongoContext
from src.schemas.data import SprintOutDTO
from src.repositories.mongo.base_crud import BaseMongoCRUD, SchemaOut
from src.schemas.user import CustomBaseModel

T = TypeVar("T", bound=CustomBaseModel)
P = ParamSpec("P")
AsyncFunc = Callable[P, Coroutine[Any, Any, Sequence[T]]]

@define
class SprintsCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'sprints' """

    collection_name: str = 'sprints'

    async def get_objects(self, out_schema: type(SchemaOut), offset: int | None = None, limit: int | None = None) -> list[SchemaOut]:
        try:
            objects = self.collection.find()
            if offset is not None:
                objects = objects.skip(offset)
            if limit is not None:
                objects = objects.limit(limit)
        except Exception as e:
            logger.error(f"Failed to find objects. {e.__class__.__name__}: {e}", )
            raise

        db_context_entities = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
        sprints = await objects.to_list()

        for sprint in sprints:
            logger.debug(f'sprint: {sprint}')
            entities = await db_context_entities.crud.get_entities_by_sprint_id(sprint['entity_ids'])

            completed_count = sum(1 for entity in entities if entity.status in ('Завершено', 'Закрыто'))
            total_count = len(entities)
            sprint['progress'] = (completed_count / total_count * 100) if total_count > 0 else 0

            sprint['update_date'] = max((entity.update_date for entity in entities if entity.update_date), default=None)

        return [out_schema(**sprint) for sprint in sprints]

    async def get_object_by_id(self, object_id: ObjectId, entities_getting_func: AsyncFunc) -> SprintOutDTO:
        logger.info('Start finding sprint')
        try:
            sprint = await self.collection.find_one({'_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise
        logger.info('Sprint found successfully')

        logger.info('Started preparing sprint model')
        if entities := sprint.get('entity_ids'):
            sprint['entities']: list[T] = await entities_getting_func(entities)
        logger.info('Sprint model prepared successfully')

        completed_count = sum(1 for entity in sprint['entities'] if entity.status in ("Завершено", "Закрыто"))
        total_count = len(sprint['entities'])

        sprint['progress'] = (completed_count / total_count * 100) if total_count > 0 else 0
        return SprintOutDTO(**sprint)