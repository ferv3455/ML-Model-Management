from signal import signal
import sqlite3
from urllib.request import proxy_bypass
import pymongo
from urllib import parse

'''
try to use noSQL:mongodb
'''

# model count
model_id_count = 0

# service count
service_id_count = 0


# connect to mongodb
'''
    connect to mongodb and set up database "mmms", you can use your own username & password in mongodb and authenticate here
'''

# data_client = pymongo.MongoClient("mongodb://localhost:27017/", username = "admin", password = "2333333")
data_client = pymongo.MongoClient("mongodb://localhost:27017/")
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

    maximum = 0
    minimum = 10000
    average = 0.0
    count = 0

    for temp_service in service_by_model:
        # init
        maximum = 0
        minimum = 10000
        average = 0.0

        temp_response = list(mongo_responses_list.find(
            {"serviceID": temp_service["id"]}))
        count = len(temp_response)

        for temp_response_one in temp_response:
            maximum = max(maximum, temp_response_one['duration'])
            minimum = min(minimum, temp_response_one['duration'])
            average = average + temp_response_one['duration']

        temp_service['count'] = count

        if (count == 0):
            temp_service['averResTime'] = '- '
            temp_service['maxResTime'] = '- '
            temp_service['minResTime'] = '- '
        else:
            temp_service['averResTime'] = '%.3f' % (1000 * average/count)
            temp_service['maxResTime'] = '%.3f' % (1000 * maximum)
            temp_service['minResTime'] = '%.3f' % (1000 * minimum)
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
    temp_service['modelID'] = modelID

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


def addPreProcess(modelID, prodes, path, name, type):
    temp_prepro = {}

    temp_prepro['modelID'] = modelID
    temp_prepro['prodes'] = prodes
    temp_prepro['path'] = path
    temp_prepro['name'] = name
    temp_prepro['type'] = type
    print(temp_prepro)

    # global preprocess_list

    # signal = False
    # for i in range(len(preprocess_list)):
    #     if preprocess_list[i]['modelID'] == modelID:
    #         preprocess_list[i]['prodes'] = prodes
    #         preprocess_list[i]['path'] = path
    #         preprocess_list[i]['name'] = name
    #         preprocess_list[i]['type'] = type
    #         signal = True
    #         break
    # if not signal:
    #     preprocess_id_count = preprocess_id_count + 1
    #     preprocess_list.append(temp_prepro)

    judge_prepro = mongo_preprocess_list.find({'modelID': modelID})
    if list(judge_prepro) == []:
        mongo_preprocess_list.insert_one(temp_prepro)
    else:
        mongo_services_list.update_one(
            {'modelID': modelID}, {'$set': {'prodes': prodes, 'path': path, 'name': name, 'type': type}})
    return


def deletePreProcess(modelID):
    # global preprocess_list

    # data_tuple = ()
    # signal = False

    # for i in range(len(preprocess_list)):
    #     if preprocess_list[i]['modelID'] == modelID:
    #         data_tuple = (
    #             True, preprocess_list[i]['prodes'], preprocess_list[i]['path'], preprocess_list[i]['name'], preprocess_list[i]['type'])
    #         preprocess_list.pop(i)
    #         preprocess_id_count = preprocess_id_count - 1
    #         signal = True
    #         break
    # if not signal:
    #     data_tuple = (False, '', '', '', '')

    judge_prepro = mongo_preprocess_list.find_one({'modelID': modelID})
    mongo_preprocess_list.delete_one({'modelID': modelID})
    print(judge_prepro)
    if judge_prepro == {}:
        return None
    else:
        return (True, judge_prepro['prodes'], judge_prepro['path'], judge_prepro['name'], judge_prepro['type'])


def getPreProcessByID(modelID):
    # global preprocess_list
    # for i in range(len(preprocess_list)):
    #     if preprocess_list[i]['modelID'] == modelID:
    #         return preprocess_list[i]
    # return None

    pro_by_id = mongo_preprocess_list.find_one({'modelID': modelID})
    if pro_by_id != None:
        pro_by_id.pop('_id')
    return pro_by_id
