from collections.abc import Mapping
from typing import Any

from attrs import define
from starlette.authentication import AuthenticationError

from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD, SchemaOut
from src.schemas.user import UserOutDTO


@define
class UsersCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'user' """

    collection_name: str = 'users'

    async def get_object_by_id(self, object_id: str) -> Any:
        return await self._get_object_by_id(object_id)

    async def get_objects(self, out_schema: type(SchemaOut), offset: int | None = None, limit: int | None = None) -> list[Mapping[str, Any]]:
        return await self._get_objects(out_schema, offset, limit)

    async def get_object_by_username(self, username: str) -> UserOutDTO:
        try:
            user = await self.collection.find_one({'username': username})
            if user is None:
                raise AuthenticationError('User not found')
        except Exception as e:
            logger.error(f"Failed to find user by id. {e.__class__.__name__}: {e}", )
            raise e

        return UserOutDTO(**user)
