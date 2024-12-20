from attrs import define

from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD
from src.schemas.user import UserOutDTO


@define
class UsersCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'user' """

    collection_name: str = 'users'

    async def get_object_by_username(self, username: str) -> UserOutDTO:
        try:
            user = self.collection.find_one({'username': username})
        except Exception as e:
            logger.error(f"Failed to find user by id. {e.__class__.__name__}: {e}", )
            raise e

        return UserOutDTO(**user)