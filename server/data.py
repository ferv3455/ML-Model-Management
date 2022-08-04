import sqlite3

'''
Initialize database columns:

TABLE models:    id (PRIMARY KEY), name, des, type, algo, time
TABLE services:  id (PRIMARY KEY), modelID, name, time, status, count
TABLE serv_response: id (PRIMARY KEY), serviceID, start, end, duration
TABLE tasks:     id (PRIMARY KEY), serviceID, modelID, time, status

(use INTEGER PRIMARY KEY for the first column so that it increments automatically)
'''


def getAllModels():
    '''Get all models from table:models. Return a list of dicts.'''
    # EXAMPLE:
    # with sqlite3.connect('database.db') as con:
    #     cur = con.cursor()
    #     cur.execute('SELECT * FROM models')
    #     records = cur.fetchall()
    #     return records


def getModelByID(modelID):
    '''Get a model from table:models. Return a dict.'''


def addModel(record):
    '''Insert a model into table:models. 
    `record` is a tuple of parameters corresponding to the columns.
    Return model ID.'''
    return 0


def getServicesByModel(modelID):
    '''Get services from table:services according to modelID. 
    For each service, look up its responses in table:serv_response, 
    and get the average, maximum and minimum time.
    Return a list of dicts.'''


def addService(record):
    '''Insert a model into table:models. 
    `record` is a tuple of parameters corresponding to the columns.
    Return service ID.'''
    return 0


def setServiceStatus(serviceID):
    '''Change service status in table:services.'''


def addResponse(serviceID, begin, end):
    '''Add a response into table:serv_response.'''


def getTasksByService(serviceID):
    '''Get tasks from table:tasks. Return a list of dicts.'''


def getTaskByID(taskID):
    '''Get a task from table:tasks. Return a dict.'''
