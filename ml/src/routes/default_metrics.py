from fastapi import APIRouter
from datetime import datetime
from src.repositories.mongo_context import MongoContext
from src.repositories.mongo import EntitiesCRUD, SprintsCRUD, HistoriesCRUD
from src.schemas.data import EntitiesOutDTO, HistoriesOutDTO, SprintsOutDTO
from fastapi.responses import JSONResponse

router = APIRouter(tags=["base endpoints"])

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
        try:
            fail, sucsess, created, ongoing = metric
        except Exception as e:
            print(e, fail, sucsess, created, ongoing)
        instance_data = self.according_to_datestamp(self.history_main_dict[key], datestamp)

        if instance_data == []:
            return fail, sucsess, created, ongoing 
        sorted_instance_data = sorted(instance_data, key=lambda x: x[1])
        # print("*******************")
        # print(sorted_instance_data)
        resolution = status = None
        for i in range(len(sorted_instance_data)):
            # print(sorted_instance_data[i])
            if sorted_instance_data[i][0] == 'Резолюция': resolution = sorted_instance_data[i][4].split(' ')[-1] if sorted_instance_data[i][4] is not None else '*'
            if sorted_instance_data[i][0] == 'Статус': status = sorted_instance_data[i][4].split(' ')[-1] if sorted_instance_data[i][4] is not None else '*'
            if sorted_instance_data[i][0] == 'Задача': status = sorted_instance_data[i][3].split(' ')[-1]if sorted_instance_data[i][3] is not None else '*'
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
    
    

@router.get('/base_metrics_left_fix')
async def get_fake_status_changes(sprint_name : str, time : datetime):
    db_context_history = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
    db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
    history_main_dict = dict()
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
    
    x = UtilitiesCalulations(history_main_dict)
    according_to_date_len = 0
    fake_changes = 0
    last_day_completions = 0
    metric= [0] * 4
    for inst in instances:
        fake_changes = x.search_through_status_changes(inst, fake_changes,  time)
        last_day_completions = x.search_for_last_day_status_change(inst, sprint_end_date, last_day_completions, time)
        metric = x.universal_sprint_counting_mashine(inst, time, metric)
        
        
        
    metrics_list = list(metric)
    metrics_list.append(fake_changes)
    metrics_list.append(last_day_completions)
    tasks_sumary = sum(metrics_list[0:5])
    metrics_list_percent = list(map(lambda x: round(x / tasks_sumary * 100), metrics_list))
    print(metrics_list)


    data = {
        "base_metrics_percentage": {
            "rapid_changes": metrics_list_percent[4],
            "last_day_completions": metrics_list_percent[5],
            "fail": metrics_list_percent[0],
            "success": metrics_list_percent[1],
            "created": metrics_list_percent[2],
            "ongoing": metrics_list_percent[3]
        },
        "base_metrics_numeric":{
            "rapid_changes": metrics_list[4],
            "last_day_completions": metrics_list[5],
            "fail": metrics_list[0],
            "success": metrics_list[1],
            "created": metrics_list[2],
            "ongoing": metrics_list[3]
        }
    }

    return JSONResponse(content=data)
    

@router.get('/base_metrics_interval')
async def get_fake_status_changes(sprint_name : str, time_left : datetime, time_right : datetime):
    time = [time_left, time_right]
    db_context_history = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
    db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
    history_main_dict = dict()
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
    
    x = UtilitiesCalulations(history_main_dict)
    fake_changes = 0
    last_day_completions = 0
    metric= [0] * 4
    for inst in instances:
        fake_changes = x.search_through_status_changes(inst, fake_changes,  time)
        last_day_completions = x.search_for_last_day_status_change(inst, sprint_end_date, last_day_completions, time)
        metric = x.universal_sprint_counting_mashine(inst, time, metric)
        
        
    metrics_list = list(metric)
    metrics_list.append(fake_changes)
    metrics_list.append(last_day_completions)
    tasks_sumary = sum(metrics_list[0:5])
    metrics_list_percent = list(map(lambda x: round(x / tasks_sumary * 100), metrics_list))
    print(metrics_list)


    data = {
        "base_metrics_percentage": {
            "rapid_changes": metrics_list_percent[4],
            "last_day_completions": metrics_list_percent[5],
            "fail": metrics_list_percent[0],
            "success": metrics_list_percent[1],
            "created": metrics_list_percent[2],
            "ongoing": metrics_list_percent[3]
        },
        "base_metrics_numeric":{
            "rapid_changes": metrics_list[4],
            "last_day_completions": metrics_list[5],
            "fail": metrics_list[0],
            "success": metrics_list[1],
            "created": metrics_list[2],
            "ongoing": metrics_list[3]
        }
    }

    return JSONResponse(content=data)


@router.get('/base_metrics_all_sprints_interval')
async def get_fake_status_changes(time_left : datetime, time_right : datetime):
    time = [time_left, time_right]
    instances = []
    db_context_history = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
    db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
    history_main_dict = dict()
    sprints_data = list(await db_context_sprints.crud.get_objects(SprintsOutDTO))
    history_data = list(await db_context_history.crud.get_objects(HistoriesOutDTO))
    for pack in sprints_data:
        instances += pack.entity_ids
        sprint_end_date = pack.sprint_end_date
    print(instances)
    for event in history_data:  
        if event.entity_id in instances:
            add_or_update_key(history_main_dict, event.entity_id, list(dict(event).values())[2:])
    
    x = UtilitiesCalulations(history_main_dict)
    fake_changes = 0
    last_day_completions = 0
    metric = [0] * 4
    for inst in instances:
        fake_changes = x.search_through_status_changes(inst, fake_changes,  time)
        last_day_completions = x.search_for_last_day_status_change(inst, sprint_end_date, last_day_completions, time)
        metric = x.universal_sprint_counting_mashine(inst, time, metric)
        
        
    metrics_list = list(metric)
    metrics_list.append(fake_changes)
    metrics_list.append(last_day_completions)
    tasks_sumary = sum(metrics_list[0:5])
    metrics_list_percent = list(map(lambda x: round(x / tasks_sumary * 100), metrics_list))
    print(metrics_list)


    data = {
        "base_metrics_percentage": {
            "rapid_changes": metrics_list_percent[4],
            "last_day_completions": metrics_list_percent[5],
            "fail": metrics_list_percent[0],
            "success": metrics_list_percent[1],
            "created": metrics_list_percent[2],
            "ongoing": metrics_list_percent[3]
        },
        "base_metrics_numeric":{
            "rapid_changes": metrics_list[4],
            "last_day_completions": metrics_list[5],
            "fail": metrics_list[0],
            "success": metrics_list[1],
            "created": metrics_list[2],
            "ongoing": metrics_list[3]
        }
    }

    return JSONResponse(content=data)
