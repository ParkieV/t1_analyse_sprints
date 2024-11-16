from attrs import define

from src.repositories.mongo.base_crud import BaseMongoCRUD


@define
class SprintsCRUD(BaseMongoCRUD):
    """ Класс для работы с коллекцией 'sprints' """

    collection_name: str = 'sprints'
