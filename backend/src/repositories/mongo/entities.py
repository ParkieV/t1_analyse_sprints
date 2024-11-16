from collections.abc import Callable, Coroutine, Sequence, Mapping
from typing import Set, TypeVar, ParamSpec, Any

from attrs import define
from bson import ObjectId

from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD, SchemaOut
from src.schemas.data import EntitiesOutDTO, EntityOutDTO
from src.schemas.user import CustomBaseModel

T = TypeVar("T", bound=CustomBaseModel)
P = ParamSpec("P")
AsyncSeqFunc = Callable[P, Coroutine[None, None, Sequence[T]]]

@define
class EntitiesCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'entities' """

    collection_name: str = 'entities'

    async def get_object_by_id(self, object_id: int) -> EntitiesOutDTO:
        logger.info('Start finding entity')
        try:
            entity = await self.collection.find_one({'entity_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise
        logger.info('Found entity successfully')

        return EntitiesOutDTO(**entity)

    async def get_objects(self, out_schema: type(SchemaOut), offset: int | None = None, limit: int | None = None) -> list[Mapping[str, Any]]:
        return await self._get_objects(out_schema, offset, limit)

    async def get_entities_by_sprint_id(self, entity_ids: list[int]) -> list[EntitiesOutDTO]:
        logger.debug(f'entity_ids: {entity_ids}')
        entities = await self.collection.find({"entity_id": {'$in': entity_ids}}).to_list()
        return [EntitiesOutDTO(**entity) for entity in entities]

    async def get_unique_areas(self) -> Set[str]:
        """ Получить уникальные области из коллекции 'entities' """
        logger.info('Fetching unique areas from entities')
        try:
            entities = await self.collection.find({}, {'area': 1}).to_list(length=None)
            unique_areas = {entity['area'] for entity in entities if isinstance(entity['area'], str)}
            logger.debug(f'Found unique areas: {unique_areas}')
        except Exception as e:
            logger.error(f"Failed to fetch unique areas. {e.__class__.__name__}: {e}")
            raise

        logger.info('Found unique areas successfully')
        return unique_areas

    async def get_object_by_id_histories(self, object_id: int, history_get_func: AsyncSeqFunc) -> EntityOutDTO:
        logger.info('Start finding entity')
        try:
            entity = await self.collection.find_one({'entity_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise
        logger.info('Entity found successfully')

        logger.info('Started preparing entity model')
        entity['history_ids'] = await history_get_func(object_id)
        logger.info('Entity model prepared successfully')

        return EntityOutDTO(**entity)