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
    def search_through_status_changes(self, key, fake_status_changes, datestamp):
        status_change_trace = []
        instance_data = self.according_to_datestamp(self.history_main_dict[key], datestamp)
        for event in instance_data:
            if event[0] == "Статус":
                status_change_trace.append(event[1])
        status_change_trace.sort()
        time_diference = []
        for i in range(1, len(status_change_trace)):
            time_diference.append((status_change_trace[i] - status_change_trace[i - 1]).total_seconds() / 60)
        if len(time_diference) != 0 and (sum(time_diference) / len(time_diference)) <= 5:
            fake_status_changes += 1
        return fake_status_changes

    def search_for_last_day_status_change(self, key, sprint_end_date, last_day_completed_counter, datestamp):
        instance_data = self.according_to_datestamp(self.history_main_dict[key], datestamp)
        for event in instance_data:
            if (event[0] == "Статус") and (event[4].split(' ')[-1] == 'closed'):
                delta_time = ((sprint_end_date - event[1])).days
                if delta_time == 0:
                    last_day_completed_counter += 1
        return last_day_completed_counter

    def universal_sprint_counting_mashine(self, key, datestamp, metric):
        fail, sucsess, created, ongoing = metric
        instance_data = self.according_to_datestamp(self.history_main_dict[key], datestamp)
        if instance_data == []:
            return fail, sucsess, created, ongoing 
        sorted_instance_data = sorted(instance_data, key=lambda x: x[1])
        # print("*******************")
        # print(sorted_instance_data)
        resolution = status = None
        for i in range(len(sorted_instance_data)):
            if sorted_instance_data[i][0] == 'Резолюция': resolution = sorted_instance_data[i][4].split(' ')[-1]
            if sorted_instance_data[i][0] == 'Статус': status = sorted_instance_data[i][4].split(' ')[-1]
            if sorted_instance_data[i][0] == 'Задача': status = sorted_instance_data[i][3].split(' ')[-1]
        # !print(status, resolution)
        if (status == 'closed' or status == 'done') and (resolution == 'Готово' or resolution == None):
            sucsess += 1
        elif (resolution in ['инициатором', 'Дубликат', 'Отклонено']):
            fail += 1 
        elif status == 'CREATED' or (status == None and resolution == None):
            created += 1
        elif status != 'closed' and status != 'CREATED':
            ongoing += 1
        return fail, sucsess, created, ongoing
    
           

@person_router.get('/person_average_compelete_time_sprint')
async def get_person_average_task_compete_time_sprint(person_name : str, sprint_name):
    try:
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
        person_average_task_time = round(sum(person_task_time) / (len(person_task_time) * 3600 * 60), 2) #hours
        
        data = {
            "average_task_time": {
                "amount": person_average_task_time,
                "quantity": "hours"
            }
        }
        
        return JSONResponse(content=data)
    except Exception as e:
            print(e)
            return JSONResponse(content={'Error ocured': e}, status=500)
        
        
@person_router.get('/person_average_compelete_time_all')
async def get_person_average_task_compete_time_all(person_name : str):
    try:
        db_context_enteties = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
        db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
        history_main_dict = dict()
        sprints_data = list(await db_context_sprints.crud.get_objects(SprintsOutDTO))
        entity_data = list(await db_context_enteties.crud.get_objects(EntitiesOutDTO))
        instances = []
        for pack in sprints_data:
            instances += pack.entity_ids
            sprint_end_date = pack.sprint_end_date
            sprint_start_date = pack.sprint_start_date
            
        person_task_time = []
        for entity in entity_data:  
            if entity.entity_id in instances and entity.assignee == person_name:
                person_task_time.append((entity.update_date - entity.create_date).total_seconds())
        print(person_task_time)
        person_average_task_time = round(sum(person_task_time) / (len(person_task_time) * 3600 * 60), 2) #hours
        
        data = {
            "average_task_time": {
                "amount": person_average_task_time,
                "quantity": "hours"
            }
        }
        
        return JSONResponse(content=data)
    except Exception as e:
            print(e)
            return JSONResponse(content={'Error ocured': e}, status=500)


@person_router.get('/person_busines_sprint')
async def get_person_busines_sprint(person_name : str, sprint_name : str):
    try:
        instances = []
        db_context_enteties = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
        db_context_history = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
        db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
        history_main_dict = dict()
        entities_main_dict = dict()
        enteties_data = list(await db_context_enteties.crud.get_objects(EntitiesOutDTO))
        sprints_data = list(await db_context_sprints.crud.get_objects(SprintsOutDTO))
        history_data = list(await db_context_history.crud.get_objects(HistoriesOutDTO))
        for pack in sprints_data:
            if pack.sprint_name == sprint_name:
                instances = pack.entity_ids
                sprint_end_date = pack.sprint_end_date
                break
            
        for event in history_data:  
            if event.entity_id in instances:
                add_or_update_key(history_main_dict, event.entity_id, list(dict(event).values())[2:])
                
        for entity in enteties_data:
            if entity.entity_id in instances:
                add_or_update_key(entities_main_dict, entity.assignee, (list(dict(entity).values())[1:]))
        
        x = UtilitiesCalulations(history_main_dict)
        
        # print(entities_main_dict.keys()) 'Н. Н.'
        metric = [0] * 4
        for person_instance in entities_main_dict[person_name]:
            inst = person_instance[0]
            metric = x.universal_sprint_counting_mashine(inst, datetime(2100, 1, 1, 1), metric)
            
        metrics_list = list(metric)
        tasks_sumary = sum(metrics_list[0:5])
        metrics_list_percent = list(map(lambda x: round(x / tasks_sumary * 100), metrics_list))
        print(metrics_list, metrics_list_percent)
        busines_percent = round(metrics_list[3] + metrics_list[2] / tasks_sumary * 100)

        return JSONResponse(content={
                    'metrics' : {
                        "fail": metrics_list[0],
                        "success": metrics_list[1],
                        "created": metrics_list[2],
                        "ongoing": metrics_list[3]
                    }, 'total' : tasks_sumary, 'busines' : {'busines_percent' : busines_percent} })
    except Exception as e:
        print(e)
        return JSONResponse(content={'Error ocured': 'error'}, status=500)
    
@person_router.get('/person_busines_all')
async def get_person_busines_all_sprints(person_name : str):
    try:
        instances = []
        db_context_enteties = MongoContext[EntitiesCRUD](crud=EntitiesCRUD())
        db_context_history = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
        db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
        history_main_dict = dict()
        entities_main_dict = dict()
        enteties_data = list(await db_context_enteties.crud.get_objects(EntitiesOutDTO))
        sprints_data = list(await db_context_sprints.crud.get_objects(SprintsOutDTO))
        history_data = list(await db_context_history.crud.get_objects(HistoriesOutDTO))
        for pack in sprints_data:
            instances += pack.entity_ids
            sprint_end_date = pack.sprint_end_date
            
        for event in history_data:  
            if event.entity_id in instances:
                add_or_update_key(history_main_dict, event.entity_id, list(dict(event).values())[2:])
                
        for entity in enteties_data:
            if entity.entity_id in instances:
                add_or_update_key(entities_main_dict, entity.assignee, (list(dict(entity).values())[1:]))
        
        x = UtilitiesCalulations(history_main_dict)
        
        # print(entities_main_dict.keys()) 'Н. Н.'
        metric = [0] * 4
        for person_instance in entities_main_dict[person_name]:
            inst = person_instance[0]
            metric = x.universal_sprint_counting_mashine(inst, datetime(2100, 1, 1, 1), metric)
            
        metrics_list = list(metric)
        tasks_sumary = sum(metrics_list[0:5])
        metrics_list_percent = list(map(lambda x: round(x / tasks_sumary * 100), metrics_list))
        print(metrics_list, metrics_list_percent)
        busines_percent = round(metrics_list[3] + metrics_list[2] / tasks_sumary * 100)

        return JSONResponse(content={
                    'metrics' : {
                        "fail": metrics_list[0],
                        "success": metrics_list[1],
                        "created": metrics_list[2],
                        "ongoing": metrics_list[3]
                    }, 'total' : tasks_sumary, 'busines' : {'busines_percent' : busines_percent} })
    except Exception as e:
        print(e)
        return JSONResponse(content={'Error ocured': 'error'}, status=500)