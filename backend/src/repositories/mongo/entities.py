import traceback
from collections.abc import Callable, Coroutine, Sequence, Mapping
from typing import TypeVar, ParamSpec, Any

from attrs import define

from src.logger import logger
from src.repositories.mongo.base_crud import BaseMongoCRUD, SchemaOut
from src.repositories.mongo_context import MongoContext
from src.schemas.data import EntitiesOutDTO, EntityOutDTO
from src.schemas.user import CustomBaseModel

T = TypeVar("T", bound=CustomBaseModel)
P = ParamSpec("P")
AsyncFunc = Callable[P, Coroutine[Any, Any, T]]
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

    async def get_unique_areas(self) -> set[str]:
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

    async def get_employees(self, employees: str | None = None, teams: str | None = None) -> list[str]:
        employee_set: set[str] = {*employees.split(',')} if employees else None
        team_list: list[str] = teams.split(',') if teams else []
        logger.debug(f'Filters: {employee_set}, {team_list}')
        try:
            employees = await self.collection.find({'area': {'$in': team_list}} if len(team_list) > 0 else {}).distinct('created_by')
            logger.debug(f'Found employees: {employees}')
            employees += await self.collection.find({'area': {'$in': team_list}} if len(team_list) > 0 else {}).distinct('updated_by')
            employees += await self.collection.find({'area': {'$in': team_list}} if len(team_list) > 0 else {}).distinct('assignee')
            employees += await self.collection.find({'area': {'$in': team_list}} if len(team_list) > 0 else {}).distinct('owner')
            employees_set = set(employees)
            if employee_set:
                employees_set.intersection_update(employee_set)
            result = []
            for employee in employees_set:
                if isinstance(employee, str):
                    result.append(employee)
            logger.debug(f'Found employees: {result}')
        except Exception as e:
            logger.error(f"Failed to fetch unique areas. {e.__class__.__name__}: {e}")
            raise

        return result

    async def get_actual_sprint(self, employee: str, get_sprint_func: AsyncFunc):
        entity_ids = await self.collection.find({'$or': [
            {'created_by': employee},
            {'updated_by': employee},
            {'assignee': employee},
            {'owner': employee}
        ]}).distinct('entity_id')

        return await get_sprint_func(entity_ids)

    async def _get_members_from_area(self, area: str) -> list[str]:
        try:
            employees = await self.collection.find({'area': area}).distinct('created_by')
            logger.debug(f'Found employees: {employees}')
            employees += await self.collection.find({'area': area}).distinct('created_by')
            employees += await self.collection.find({'area': area}).distinct('updated_by')
            employees += await self.collection.find({'area': area}).distinct('assignee')
            employees += await self.collection.find({'area': area}).distinct('owner')
            employees_set = set(employees)
            result = []
            for employee in employees_set:
                if isinstance(employee, str):
                    result.append(employee)
            logger.debug(f'Found employees: {result}')
        except Exception as e:
            logger.error(f"Failed to fetch unique areas. {e.__class__.__name__}: {e}")
            raise

        return result

    async def get_teams_with_members(self) -> Mapping[str, list[str]]:
        try:
            teams = await self.collection.distinct('area')
            return {team: await self._get_members_from_area(team) for team in teams}
        except Exception:
            logger.error(f"Failed to fetch unique areas. {traceback.format_exc()}")
            raise