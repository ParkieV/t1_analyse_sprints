from fastapi import APIRouter
from datetime import datetime
from src.repositories.mongo_context import MongoContext
from src.repositories.mongo import EntitiesCRUD, SprintsCRUD, HistoriesCRUD
from src.schemas.data import EntitiesOutDTO, HistoriesOutDTO, SprintsOutDTO
from fastapi.responses import JSONResponse

add_router = APIRouter(tags=["endpoints with additional metrics"])

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
    
    def late_create_searcher(self, key, late_create, datestamp, sprint_start_date):
        instance_data = self.according_to_datestamp(self.history_main_dict[key], datestamp)
        for i in range(len(instance_data)):
                # print(instance_data[i], (instance_data[i][3] == 'CREATED'), ((instance_data[i][1] - datestamp).days > 2))
            if (instance_data[i][3] == 'CREATED') and ((instance_data[i][1] - sprint_start_date).days > 2):
                
                late_create += 1
                break
        return late_create
           

@add_router.get('/backlog_change')
async def get_backlog_change(sprint_name : str, time : datetime):
    try:
        db_context_history = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
        db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
        history_main_dict = dict()
        sprints_data = list(await db_context_sprints.crud.get_objects(SprintsOutDTO))
        history_data = list(await db_context_history.crud.get_objects(HistoriesOutDTO))
        for pack in sprints_data:
            if pack.sprint_name == sprint_name:
                instances = pack.entity_ids
                sprint_end_date = pack.sprint_end_date
                sprint_start_date = pack.sprint_start_date
                if (time - sprint_start_date).days <= 2:
                    return JSONResponse(content={"backlog_changed_persents": 0})
        
        for event in history_data:  
            if event.entity_id in instances:
                add_or_update_key(history_main_dict, event.entity_id, list(dict(event).values())[2:])
        
        x = UtilitiesCalulations(history_main_dict)
        late_create =  0
        for inst in instances:
            late_create = x.late_create_searcher(inst, late_create, time, sprint_start_date)

        data = {
            "backlog_changed_persents": round(late_create / len(instances) * 100),
            "Status" : "Good" if (value := round(late_create / len(instances) * 100)) < 20 else ("OK" if value <= 50 else "Bad")
        }

        return JSONResponse(content=data)
    except Exception as e:
            print(e)
            return JSONResponse(content={'Error ocured': e}, status=500)


@add_router.get('/backlog_change_interval')
async def get_backlog_change(sprint_name : str, time_left : datetime, time_right : datetime):
    try:
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
                sprint_start_date = pack.sprint_start_date
                if (time_left - sprint_start_date).days <= 2 and (time_right - sprint_start_date).days <= 2:
                    return JSONResponse(content={"backlog_changed_persents": 0, "Status" : "Good"})
        
        for event in history_data:  
            if event.entity_id in instances:
                add_or_update_key(history_main_dict, event.entity_id, list(dict(event).values())[2:])
        
        x = UtilitiesCalulations(history_main_dict)
        late_create =  0
        for inst in instances:
            late_create = x.late_create_searcher(inst, late_create, time, sprint_start_date)

        data = {
            "backlog_changed_persents": round(late_create / len(instances) * 100),
            "Status" : "Good" if (value := round(late_create / len(instances) * 100)) < 20 else ("OK" if value <= 50 else "Bad")
        }
        return JSONResponse(content=data)
    except Exception as e:
        print(e)
        return JSONResponse(content={'Error ocured': e}, status=500)
    

@add_router.get('/backlog_change_all_sprints_interval')
async def get_backlog_change(time_left : datetime, time_right : datetime):
    try:
        time = [time_left, time_right]
        db_context_history = MongoContext[HistoriesCRUD](crud=HistoriesCRUD())
        db_context_sprints = MongoContext[SprintsCRUD](crud=SprintsCRUD())
        history_main_dict = dict()
        sprints_data = list(await db_context_sprints.crud.get_objects(SprintsOutDTO))
        history_data = list(await db_context_history.crud.get_objects(HistoriesOutDTO))
        instances = []
        for pack in sprints_data:
            instances += pack.entity_ids
            sprint_end_date = pack.sprint_end_date
            sprint_start_date = pack.sprint_start_date
            if (time_left - sprint_start_date).days <= 2 and (time_right - sprint_start_date).days <= 2:
                return JSONResponse(content={"backlog_changed_persents": 0, "Status" : "Good"})
            
        
        for event in history_data:  
            if event.entity_id in instances:
                add_or_update_key(history_main_dict, event.entity_id, list(dict(event).values())[2:])
        
        x = UtilitiesCalulations(history_main_dict)
        late_create =  0
        for inst in instances:
            late_create = x.late_create_searcher(inst, late_create, time, sprint_start_date)

        data = {
            "backlog_changed_persents": round(late_create / len(instances) * 100),
            "Status" : "Good" if (value := round(late_create / len(instances) * 100)) < 20 else ("OK" if value <= 50 else "Bad")
        }
        return JSONResponse(content=data)
    except Exception as e:
            print(e)
            return JSONResponse(content={'Error ocured': e}, status=500)

# @add_router.get('/blocked_in_hh')
# async def get_backlog_change(time_left : datetime, time_right : datetime):
