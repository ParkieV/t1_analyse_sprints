import json
from typing import Literal

from src.logger import logger
from src.repositories.mongo import EntitiesCRUD, HistoriesCRUD, SprintsCRUD
from src.repositories.mongo_context import MongoContext

db_context = MongoContext()

async def add_data_to_db(data, data_type: Literal['entities', 'histories', 'sprints']):
    if data_type == 'entities':
        logger.info('Data about entities')
        db_context.crud = EntitiesCRUD()
        logger.debug('Inserting entities')
        await db_context.crud.insert_objects(data)

    elif data_type == 'histories':
        logger.info('Data about histories')
        db_context.crud = HistoriesCRUD()
        logger.debug('Inserting histories')
        await db_context.crud.insert_objects(data)

    elif data_type == 'sprints':
        logger.info('Data about sprints')
        for row in data:
            row['entity_ids'] = [int(x) for x in row["entity_ids"].strip('{}').split(',')]

        db_context.crud = SprintsCRUD()
        logger.debug('Inserting sprints')
        await db_context.crud.insert_objects(data)