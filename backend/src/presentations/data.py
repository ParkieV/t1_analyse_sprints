from doctest import debug

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
import pandas as pd
from jose import jwt, JWTError

from src.config import auth_config
from src.jwt import AuthHandler
from src.logger import logger
from src.services.parse_data import add_data_to_db

router = APIRouter(prefix="/data", tags=["Data endpoints"])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...),
                      token: str = Depends(AuthHandler.oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, auth_config.secret_key, algorithms=[auth_config.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

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
