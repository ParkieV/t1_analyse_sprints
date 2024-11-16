from attrs import define

from src.repositories.mongo.base_crud import BaseMongoCRUD


@define
class EntitiesCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'entities' """

    collection_name: str = 'entities'
