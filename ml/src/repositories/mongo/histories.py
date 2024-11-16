from attrs import define

from src.repositories.mongo.base_crud import BaseMongoCRUD


@define
class HistoriesCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'histories' """

    collection_name: str = 'histories'
