import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status

from src.logger import logger
from src.schemas.data import EntitiesOutDTO, HistoriesOutDTO, SprintsOutDTO
from src.services.utils import check_token
from src.repositories.mongo import EntitiesCRUD, SprintsCRUD, HistoriesCRUD
from src.services.parse_data import add_data_to_db
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


@router.get('/histories', dependencies=[Depends(check_token)])
async def get_entities(page_number: int,
                       page_size: int = 15):
    db_context = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
    return await db_context.crud.get_objects(HistoriesOutDTO, (page_number - 1) * page_size, page_size)


@router.get('/sprints', dependencies=[Depends(check_token)])
async def get_entities(page_number: int,
                       page_size: int = 15):
    db_context = MongoContext[SprintsCRUD](crud=SprintsCRUD())
    return await db_context.crud.get_objects(SprintsOutDTO, (page_number - 1) * page_size, page_size)