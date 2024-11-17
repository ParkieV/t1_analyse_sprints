import pandas as pd
from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from rapidfuzz import process, fuzz

from src.logger import logger
from src.schemas.data import EntitiesOutDTO, HistoriesOutDTO, SprintsOutDTO
from src.services.utils import check_token
from src.repositories.mongo import EntitiesCRUD, SprintsCRUD, HistoriesCRUD
from src.services.parse_data import add_data_to_db, db_context
from src.repositories.mongo_context import MongoContext

router = APIRouter(prefix="/data", tags=["Data endpoints"])


@router.post("/upload", dependencies=[Depends(check_token)], status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    try:
        skip_first_row: bool = ('Table' in str(file.file.readline()))

        file.file.seek(0)
        df = pd.read_csv(file.file, sep=';', skiprows=int(skip_first_row))
        df_cleaned = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
        data_dicts = df_cleaned.to_dict(orient='records')
        logger.debug(f"First 2 row: {data_dicts[:2]}")

        logger.info('Data parsed successfully')
    except Exception as e:
        logger.error("Failed to read file: %s - %s", e.__class__.__name__, e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not read file')

    try:
        logger.info('Start loading data')

        logger.debug("last column: %s", df_cleaned.columns[-1])
        if df_cleaned.columns[-1] == 'entity_ids':
            await add_data_to_db(data_dicts, 'sprints')
        elif df_cleaned.columns[-1] == 'resolution':
            await add_data_to_db(data_dicts, 'entities')
        elif df_cleaned.columns[-1] == 'history_change':
            await add_data_to_db(data_dicts, 'histories')
        else:
            raise ValueError('Could not identify dataset')

        logger.info('Data loaded successfully!')
    except Exception as e:
        logger.error("Failed to load file: %s - %s", e.__class__.__name__, e)
        if e.__class__.__name__ == 'ValueError' and e.args[0] == 'Could not identify dataset':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not read this file')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Loading data failed')


@router.get('/entities', dependencies=[Depends(check_token)])
async def get_entities(page_number: int,
                       page_size: int = 15):

    db_context = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
    return await db_context.crud.get_objects(EntitiesOutDTO, (page_number - 1) * page_size, page_size)

@router.get('/entities/{entity_id}', dependencies=[Depends(check_token)])
async def get_entity(entity_id: int):
    db_context_entities = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
    db_context_histories = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())

    return await db_context_entities.crud.get_object_by_id_histories(entity_id, db_context_histories.crud.get_objects_by_entity_id)


@router.get('/histories', dependencies=[Depends(check_token)])
async def get_histories(page_number: int,
                       page_size: int = 15):
    db_context = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
    return await db_context.crud.get_objects(HistoriesOutDTO, (page_number - 1) * page_size, page_size)


@router.get('/sprints', dependencies=[Depends(check_token)])
async def get_sprints(page_number: int,
                       page_size: int = 15):
    db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())

    sprints = await db_context_sprints.crud.get_objects(SprintsOutDTO, (page_number - 1) * page_size, page_size)

    return sprints


@router.get('/areas', dependencies=[Depends(check_token)])
async def get_areas():
    db_context = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
    return await db_context.crud.get_unique_areas()

@router.get('/change_types', dependencies=[Depends(check_token)])
async def get_change_types():
    db_context = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
    return await db_context.crud.get_change_types()

@router.get('/sprints/{sprint_id}', dependencies=[Depends(check_token)])
async def get_sprint(sprint_id: str):
    try:
        obj_sprint_id = ObjectId(sprint_id)
    except Exception as e:
        logger.error("Could not read 'sprint_id': %s - %s", e.__class__.__name__, e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="parameter 'sprint_id' is invalid")

    db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
    db_context_entities = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
    
    sprint = await db_context_sprints.crud.get_object_by_id(obj_sprint_id, db_context_entities.crud.get_entities_by_sprint_id)

    return sprint

@router.get('/employees', dependencies=[Depends(check_token)])
async def get_employees(employees: str | None = None, teams: str | None = None):
    db_context_entities = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
    db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())

    employees = await db_context_entities.crud.get_employees(employees, teams)
    employees_list = []
    for employee in employees:
        employee_dict = {}
        employee_dict['employee'] = employee
        employee_dict['sprint'] = await db_context_entities.crud.get_actual_sprint(employee, db_context_sprints.crud.get_last_sprint)
        logger.debug(employee_dict['sprint'])
        employees_list.append(employee_dict)
    return employees_list

@router.get('/commands', dependencies=[Depends(check_token)])
async def get_teams():
    db_context = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
    return await db_context.crud.get_teams_with_members()

@router.get('/search/sprints', dependencies=[Depends(check_token)])
async def get_sprints(search_query: str):
    db_context = MongoContext[SprintsCRUD](crud=SprintsCRUD())

    data = await db_context.crud.get_column_values('sprint_name')
    logger.debug(f'sprint data: {data}')
    data_df = pd.DataFrame(data, columns=['sprint_name'])

    matches = process.extract(search_query, data, scorer=fuzz.ratio)
    logger.debug(f'matches: {matches}')

    threshold = 68
    matched_values = [match[0] for match in matches if match[1] >= threshold]
    result = data_df[data_df['sprint_name'].isin(matched_values)]
    logger.debug(f'Results: {result}')

    return result

@router.get('/search/entities', dependencies=[Depends(check_token)])
async def get_entities(search_query: str):
    db_context = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())

    data = await db_context.crud.get_column_values('name')
    logger.debug(f'entity data: {data}')
    data_df = pd.DataFrame(data, columns=['name'])

    matches = process.extract(search_query, data, scorer=fuzz.ratio)
    logger.debug(f'matches: {matches}')

    threshold = 20
    matched_values = [match[0] for match in matches if match[1] >= threshold]
    result = data_df[data_df['name'].isin(matched_values)]
    logger.debug(f'Results: {result}')

    return result

@router.get('/search/histories', dependencies=[Depends(check_token)])
async def get_histories(search_query: str):
    db_context = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())

    data = await db_context.crud.get_column_values('history_property_name')
    logger.debug(f'entity data: {data}')
    data_df = pd.DataFrame(data, columns=['history_property_name'])

    matches = process.extract(search_query, data, scorer=fuzz.ratio)
    logger.debug(f'matches: {matches}')

    threshold = 20
    matched_values = [match[0] for match in matches if match[1] >= threshold]
    result = data_df[data_df['history_property_name'].isin(matched_values)]
    logger.debug(f'Results: {result}')

    return result