from typing import Any

from attrs import define
from pyasn1.type.univ import Sequence

from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD
from src.schemas.data import HistoriesOutDTO


@define
class HistoriesCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'histories' """

    collection_name: str = 'histories'

    async def get_object_by_id(self, object_id: str) -> Any:
        return await self._get_object_by_id(object_id)

    async def get_object_by_entity_id(self, entity_id: int) -> list[HistoriesOutDTO]:
        logger.info('Start finding histories')
        try:
            histories = self.collection.find({'entity_id': entity_id})
        except Exception as e:
            logger.error("Error finding histories: %s - %s", e.__class__.__name__, e)
            raise
        logger.info('Found histories successfully')

        return [HistoriesOutDTO(**history) for history in histories]