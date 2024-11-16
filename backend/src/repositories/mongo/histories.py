from collections.abc import Mapping
import math
from typing import Any, Set

from attrs import define

from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD, SchemaOut
from src.schemas.data import EntitiesOutDTO, HistoriesOutDTO


@define
class HistoriesCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'histories' """

    collection_name: str = 'histories'

    async def get_object_by_id(self, object_id: str) -> Any:
        return await self._get_object_by_id(object_id)

    async def get_objects(self, out_schema: type(SchemaOut), offset: int | None = None, limit: int | None = None) -> list[Mapping[str, Any]]:
        return await self._get_objects(out_schema, offset, limit)

    async def get_objects_by_entity_id(self, entity_id: int) -> list[HistoriesOutDTO]:
        logger.info('Start finding histories')
        try:
            histories = self.collection.find({'entity_id': entity_id})
        except Exception as e:
            logger.error("Error finding histories: %s - %s", e.__class__.__name__, e)
            raise
        logger.info('Found histories successfully')

        return [HistoriesOutDTO(**history) for history in histories]

    async def get_change_types(self) -> Set[str]:
        """ Получить уникальные области из коллекции 'histories' """
        logger.info('Fetching unique change_types from histories')
        try:
            histories = self.collection.find({}, {'history_change_type': 1}).to_list(length=None)
            change_types = {history['history_change_type'] for history in histories if isinstance(history['history_change_type'], str)}
            logger.info(f'Found unique change_types: {change_types}')
            return change_types
        except Exception as e:
            logger.error(f"Failed to fetch unique change_types. {e.__class__.__name__}: {e}")
            raise
