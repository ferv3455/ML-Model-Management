from signal import signal
import sqlite3
import pymongo
from urllib import parse
# all active services

'''
Initialize database columns:

TABLE models:    id (PRIMARY KEY), name, des, type, algo, time
TABLE services:  id (PRIMARY KEY), modelID, name, time, status, count
TABLE serv_response: id (PRIMARY KEY), serviceID, start, end, duration
TABLE tasks:     id (PRIMARY KEY), serviceID, modelID, time, status

(use INTEGER PRIMARY KEY for the first column so that it increments automatically)
'''

'''
function list:

FUNCTION getAllModels
FUNCTION getModelByID(modelID): get model by modelID
FUNCTION addModel(record)

FUNCTION getServicesByModel(modelID): get all services have this modelID
FUNCTION addService(modelID, name, time, status, count)
FUNCTION setServiceStatus(serviceID,status)

FUNCITON addResponse(serviceID, begin, end)
FUNCTION getTasksByService(serviceID)
FUNCTION getTaskByID(taskID)
FUNCTION newTask()

'''

'''
try to use noSQL:mongodb
'''
# models\response
models_list = []
services_list = []
response_list = []
tasks_list = []
preprocess_list = []

# model count
model_id_count = 0

# service count
service_id_count = 0

# task count
task_id_count = 0

# preprocess count
preprocess_id_count = 0

# connect to mongodb
'''
    connect to mongodb and set up database "mmms", you can use your own username & password in mongodb and authenticate here
'''

# data_client = pymongo.MongoClient("mongodb://localhost:27017/", username = "admin", password = "2333333")
data_client = pymongo.MongoClient(
    "mongodb://localhost:27017/")
data_base = data_client['mmms']


def data_base_init():
    collection_names = data_base.list_collection_names()  # 获取数据库中所有的 collection 名称
    for collection_name in collection_names:
        # 每个数据库包含多个集合，根据集合名称获取集合对象（Collection）
        db_collection = data_base[collection_name]
        db_collection.delete_many({})


data_base_init()  # clear previous data

# set up lists in data_base
mongo_models_list = data_base['mongo_models_list']
mongo_services_list = data_base['mongo_services_list']
mongo_responses_list = data_base['mongo_response_list']
mongo_tasks_list = data_base['mongo_tasks_list']
mongo_preprocess_list = data_base['mongo_preprocess_list']


def getAllModels():
    '''Get all models from table:models. Return a list of dicts.'''

    all_models_list = list(mongo_models_list.find())
    # print('all_model:')
    # print(all_models_list)
    # return all_models_list
    return all_models_list
    # EXAMPLE:
    # with sqlite3.connect('database.db') as con:
    #     cur = con.cursor()
    #     cur.execute('SELECT * FROM models')
    #     records = cur.fetchall()
    #     return records


# def getModelByID(modelID):
#     '''Get a model from table:models. Return a dict.'''
#     for temp_model in models_list:
#         if temp_model['id'] == modelID:
#             return temp_model
#     return None

def getModelByID(modelID):
    '''Get a model from table:models. Return a dict.'''
    model_by_id = mongo_models_list.find_one({"id": modelID})
    return model_by_id


def addModel(record):  # add new model to models_list
    '''Insert a model into table:models.
    `record` is a tuple of parameters corresponding to the columns.
    Return model ID.'''

    # use dict as element in model, to easily get model by id
    param_names = ('name', 'des', 'type', 'algo', 'time')
    temp_dict = dict(zip(param_names, record))

    global model_id_count
    temp_dict['id'] = model_id_count
    model_id_count = model_id_count+1
    # models_list.append(temp_dict)

    # model_mongo_id = mongo_models_list.insert_one(temp_dict) 返回值为id
    mongo_models_list.insert_one(temp_dict)

    return model_id_count-1


def deleteModel(modelID):
    # for temp_model in models_list:
    #     if temp_model['id'] == modelID:
    #         models_list.remove(temp_model)
    mongo_models_list.delete_one({"id": modelID})
    return


def getServicesByModel(modelID):
    '''Get services from table:services according to modelID.
    For each service, look up its responses in table:serv_response,
    and get the average, maximum and minimum time.
    Return a list of dicts.'''

    # records = []

    # for temp_service in services_list:
    #     if temp_service['modelID'] == modelID:
    #         # TODO:search in response and find the times
    #         records.append(temp_service)
    # return records

    service_by_model = list(mongo_services_list.find({"modelID": modelID}))
    return service_by_model

# new a service


def addService(modelID, name, time, status, count):
    '''Insert a service into table:services.
       Return service ID.'''
    temp_service = {}

    global service_id_count

    temp_service['id'] = service_id_count
    temp_service['name'] = name
    temp_service['time'] = time
    temp_service['status'] = status
    temp_service['count'] = count
    temp_service['modelID'] = modelID
    temp_service['averResTime'] = 0
    temp_service['maxResTime'] = 0
    temp_service['minResTime'] = 0

    service_id_count = service_id_count+1

    # services_list.append(temp_service)
    mongo_services_list.insert_one(temp_service)

    return service_id_count-1


def setServiceStatus(serviceID, status):
    '''Change service status in table:services.'''

    # for temp_service in services_list:
    #     if temp_service['id'] == serviceID:
    #         if (status == 'delete'):
    #             services_list.remove(temp_service)
    #             return
    #         else:
    #             temp_service['status'] = status
    #             return

    if status == 'delete':
        mongo_services_list.delete_many(
            {'id': serviceID})
    else:
        mongo_services_list.update_many(
            {'id': serviceID}, {'$set': {'status': status}})
    return


def addResponse(serviceID, begin, end):
    '''Add a response into table:serv_response.'''
    temp_response = {}

    temp_response['serviceID'] = serviceID
    temp_response['begin'] = begin
    temp_response['end'] = end
    temp_response['duration'] = end-begin

    # response_list.append(temp_response)
    mongo_responses_list.insert_one(temp_response)

    return


def getTasksByService(serviceID):
    '''Get tasks from table:tasks. Return a list of dicts.'''

    # records = []

    # for temp_task in tasks_list:
    #     if temp_task['serviceID'] == serviceID:
    #         records.append(temp_task)

    task_by_service = list(mongo_services_list.find({"serviceID": serviceID}))
    return task_by_service

    # return records


def getTaskByID(taskID):
    '''Get a task from table:tasks. Return a dict.'''
    for temp_task in tasks_list:
        if temp_task['taskID'] == taskID:
            return temp_task
    return {}


def newTask():
    '''new a task to table:tasks.
    Return taskID'''
    temp_task = {}
    temp_task['taskID'] = task_id_count

    # TODO: other imformation of task

    task_id_count = task_id_count+1
    return task_id_count-1


def addPreProcess(modelID, prodes, path, name, type):
    prepro = {}
    prepro['modelID'] = modelID
    prepro['prodes'] = prodes
    prepro['path'] = path
    prepro['name'] = name
    prepro['type'] = type
    global preprocess_id_count
    global preprocess_list
    signal = False
    for i in range(len(preprocess_list)):
        if preprocess_list[i]['modelID'] == modelID:
            preprocess_list[i]['prodes'] = prodes
            preprocess_list[i]['path'] = path
            preprocess_list[i]['name'] = name
            preprocess_list[i]['type'] = type
            signal = True
            break
    if not signal:
        preprocess_id_count = preprocess_id_count + 1
        preprocess_list.append(prepro)

    return preprocess_id_count


def deletePreProcess(modelID):
    global preprocess_list
    global preprocess_id_count
    data_tuple = ()
    signal = False
    for i in range(len(preprocess_list)):
        if preprocess_list[i]['modelID'] == modelID:
            data_tuple = (
                True, preprocess_list[i]['prodes'], preprocess_list[i]['path'], preprocess_list[i]['name'], preprocess_list[i]['type'])
            preprocess_list.pop(i)
            preprocess_id_count = preprocess_id_count - 1
            signal = True
            break
    if not signal:
        data_tuple = (False, '', '', '', '')

    return data_tuple


def getPreProcessByID(modelID):
    global preprocess_list
    for i in range(len(preprocess_list)):
        if preprocess_list[i]['modelID'] == modelID:
            return preprocess_list[i]
    return None
