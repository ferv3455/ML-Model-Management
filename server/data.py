import sqlite3
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
# models\response
models_list = []
services_list = []
response_list = []
tasks_list = []

# model count
model_id_count = 0

# service count
service_id_count = 0

# task count
task_id_count = 0


def getAllModels():
    '''Get all models from table:models. Return a list of dicts.'''
    return models_list
    # EXAMPLE:
    # with sqlite3.connect('database.db') as con:
    #     cur = con.cursor()
    #     cur.execute('SELECT * FROM models')
    #     records = cur.fetchall()
    #     return records


def getModelByID(modelID):
    '''Get a model from table:models. Return a dict.'''
    print(models_list)
    for temp_model in models_list:
        if temp_model['id'] == modelID:
            return temp_model
    zero_model = {}
    return zero_model


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
    models_list.append(temp_dict)
    return model_id_count-1


def getServicesByModel(modelID):
    '''Get services from table:services according to modelID.
    For each service, look up its responses in table:serv_response,
    and get the average, maximum and minimum time.
    Return a list of dicts.'''
    records = []

    for temp_service in services_list:
        if temp_service['modelID'] == modelID:
            # TODO:search in response and find the times
            records.append(temp_service)
    return records

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

    services_list.append(temp_service)
    return service_id_count-1


def setServiceStatus(serviceID, status):
    '''Change service status in table:services.'''
    for temp_service in services_list:
        if temp_service['id'] == serviceID:
            if (status == 'delete'):
                services_list.remove(temp_service)
                return
            else:
                temp_service['status'] = status
                return


def addResponse(serviceID, begin, end):
    '''Add a response into table:serv_response.'''
    temp_response = {}

    temp_response['serviceID'] = serviceID
    temp_response['begin'] = begin
    temp_response['end'] = end
    temp_response['duration'] = end-begin

    response_list.append(temp_response)
    return


def getTasksByService(serviceID):
    '''Get tasks from table:tasks. Return a list of dicts.'''
    records = []

    for temp_task in tasks_list:
        if temp_task['serviceID'] == serviceID:
            records.append(temp_task)

    return records


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
