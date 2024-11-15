from uuid import UUID

from pymongo.database import Database
from pymongo.collection import Collection

from src.logger import logger

class BaseMongoCRUD:
    collection: Collection

    def __init__(self, db: Database, collection_name: str) -> None:
        self.collection = db[collection_name]

    async def get_object_by_id(self, object_id: UUID):
        try:
            user = self.collection.find_one({'_id': object_id})
        except Exception as e:
            logger.error(f"Failed to find user by id. {e.__class__.__name__}: {e}", )
            raise e

        return user