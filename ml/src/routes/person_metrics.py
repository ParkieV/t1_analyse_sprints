from fastapi import APIRouter
from datetime import datetime
from src.repositories.mongo_context import MongoContext
from src.repositories.mongo import EntitiesCRUD, SprintsCRUD, HistoriesCRUD
from src.schemas.data import EntitiesOutDTO, HistoriesOutDTO, SprintsOutDTO
from fastapi.responses import JSONResponse

person_router = APIRouter(tags=["endpoints with person metrics"])

def add_or_update_key(dictionary : dict, key, value_to_add):
    dictionary[key] = dictionary.setdefault(key, [])
    dictionary[key].append(value_to_add)

class UtilitiesCalulations:
    def __init__(self, history_main_dict):
        self.history_main_dict = history_main_dict   
        
    def according_to_datestamp(self, d2_array, datestamp):
        res = []
        for inst in d2_array:
            if type(datestamp) == list:
                if datestamp[0] <= inst[1] <= datestamp[1]:
                    res.append(inst)
            else:
                if inst[1] <= datestamp:
                    res.append(inst)
        return res
    
           

@person_router.get('/person_average_compelete_time_sprint')
async def get_backlog_change(person_name : str, sprint_name, time_left : datetime, time_right : datetime):
    db_context_enteties = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
    db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
    history_main_dict = dict()
    sprints_data = list(await db_context_sprints.crud.get_objects(SprintsOutDTO))
    entity_data = list(await db_context_enteties.crud.get_objects(EntitiesOutDTO))
    for pack in sprints_data:
        if pack.sprint_name == sprint_name:
            instances = pack.entity_ids
            sprint_end_date = pack.sprint_end_date
            sprint_start_date = pack.sprint_start_date
            break
    person_task_time = []
    for entity in entity_data:  
        if entity.entity_id in instances and entity.assignee == person_name:
            person_task_time.append((entity.update_date - entity.create_date).total_seconds())
    print(person_task_time)
    person_average_task_time = round(sum(person_task_time) / (len(person_task_time) * 3600), 2) #hours
    
    data = {
        "average_task_time": {
            "amount": person_average_task_time,
            "quantity": "hours"
        }
    }
    
    return JSONResponse(content=data)