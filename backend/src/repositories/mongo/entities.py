from typing import Any

from attrs import define

from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD
from src.schemas.data import EntitiesOutDTO


@define
class EntitiesCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'entities' """

    collection_name: str = 'entities'

    async def get_object_by_id(self, object_id: int) -> EntitiesOutDTO:
        logger.info('Start finding entity')
        try:
            entity = self.collection.find_one({'entity_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find object by id. {e.__class__.__name__}: {e}", )
            raise
        logger.info('Found entity successfully')

        return EntitiesOutDTO(**entity)