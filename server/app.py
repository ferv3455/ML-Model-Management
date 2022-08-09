from datetime import datetime
import traceback
import os

from gevent import pywsgi
from flask import Flask, jsonify, request
from flask_cors import CORS

from model import Model
from service import Service, ServiceList
import data
from fileReader import readCSV, readZIP


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, supports_credentials=True)

# all active services
global services
services = ServiceList()

# View functions begin
# TODO: It should be full of BUUUUUUGS now


@app.route('/model', methods=['GET'])
def getAllModels():
    print('Getting all models')
    try:
        param_names = ('id', 'name', 'des', 'type', 'algo', 'time')
        res = {'models': [{key: m[key] for key in param_names}
                          for m in data.getAllModels()]}
    except:
        traceback.print_exc()
        res = {'models': []}

    return jsonify(res)


@app.route('/model', methods=['POST'])
def createModel():
    try:
        params = request.form.to_dict()  # keys: name, des, type, file
        print('Creating model:', params)

        id = data.model_id_count
        params['file'] = './models/{}.{}'.format(id, params['type'])
        request.files['file'].save(params['file'])
        model = Model(**params)

        param_names = ('name', 'des', 'type', 'algo', 'time')
        data.addModel(tuple(getattr(model, key) for key in param_names))

        res = {'status': 'success'}

    except Exception as exc:
        traceback.print_exc()
        res = {
            'status': 'fail',
            'reason': exc
        }

    return jsonify(res)


@app.route('/model/<int:modelID>', methods=['GET'])
def getModelInfo(modelID):
    model_params = data.getModelByID(modelID)
    print(model_params)
    res = {'exist': (model_params is not None)}
    print('Searching for model {}: {}'.format(modelID, res['exist']))

    if res['exist']:
        try:
            model = Model(model_params['name'],
                          model_params['des'], model_params['type'],
                          './models/{}.{}'.format(modelID, model_params['type']))
            param_names = ('name', 'des', 'type', 'algo',
                           'time', 'input', 'output')
            res.update({key: getattr(model, key) for key in param_names})
            print(res)
        except:
            traceback.print_exc()

    return jsonify(res)


@app.route('/model/<int:modelID>/test', methods=['POST'])
def testModel(modelID):
    try:
        input_data = request.get_json()['submitObject']
        print('Testing on model {}: {}'.format(modelID, input_data))
        model_params = data.getModelByID(modelID)
        print(model_params)
        model = Model(model_params['name'],
                      model_params['des'], model_params['type'],
                      './models/{}.{}'.format(modelID, model_params['type']))
        result = model.predict(input_data)
        res = {'output': result}
    except:
        traceback.print_exc()
        res = None

    return jsonify(res)


@app.route('/model/<int:modelID>/service', methods=['GET'])
def getAllServices(modelID):
    print('Getting all services of model {}'.format(modelID))
    try:
        records = data.getServicesByModel(modelID)
        param_names = ('id', 'name', 'time', 'status', 'count',
                       'averResTime', 'maxResTime', 'minResTime')
        res = {'services': [{key: r[key]
                             for key in param_names} for r in records]}
    except:
        traceback.print_exc()
        res = {'services': []}

    return jsonify(res)


@app.route('/model/<int:modelID>/service', methods=['POST'])
def createService(modelID):
    try:
        params = request.get_json()  # keys: name
        print('Creating service:', params)
        serviceID = data.addService(
            modelID, params['name'], datetime.now(), 'running', 0)

        model_params = data.getModelByID(modelID)
        model = Model(model_params['name'],
                      model_params['des'], model_params['type'],
                      './models/{}.{}'.format(modelID, model_params['type']))
        services.add(serviceID, Service(serviceID, model, modelID))
        res = {'status': 'success'}

    except Exception as exc:
        traceback.print_exc()
        res = {
            'status': 'fail',
            'reason': exc
        }
    return jsonify(res)


@app.route('/model/<int:modelID>/service/<int:serviceID>', methods=['POST'])
def changeServiceStatus(modelID, serviceID):
    begin = datetime.now()

    try:
        cmd = request.get_json()
        status = cmd['opr']
        print('Change service {}/{} status to {}'.format(modelID, serviceID, status))

        data.setServiceStatus(serviceID, status)
        if status == 'start' or status == 'pause':
            services.get(serviceID).changeStatus(status)
        else:
            services.delete(serviceID)

        res = {'status': 'success'}
    except:
        traceback.print_exc()
        res = {'status': 'fail'}

    end = datetime.now()
    data.addResponse(serviceID, begin, end)
    return jsonify(res)


@app.route('/model/<int:modelID>/service/<int:serviceID>/quick', methods=['POST'])
def quickPredict(modelID, serviceID):
    print('Quick Predict on model {}, service {}'.format(modelID, serviceID))
    begin = datetime.now()

    try:
        service = services.get(serviceID)
        input_data = request.get_json()
        result = service.predict(input_data)
        res = {'output': result}
    except:
        traceback.print_exc()
        res = None

    end = datetime.now()
    data.addResponse(serviceID, begin, end)

    return jsonify(res)


@app.route('/model/<int:modelID>/service/<int:serviceID>/task', methods=['POST'])
def batchPredict(modelID, serviceID):
    print('Batch Predict on model {}, service {}'.format(modelID, serviceID))
    begin = datetime.now()

    try:
        service = services.get(serviceID)
        batch_data = request.files['file']
        _, ext = os.path.splitext(batch_data.filename)

        if ext == '.csv':
            data_gen = readCSV(batch_data)
        elif ext == '.zip':
            data_gen = readZIP(batch_data)
        else:
            raise ValueError('File format not readable')

        taskID = service.batch(data_gen)
        res = {'id': taskID}
        batch_data.close()
    except:
        traceback.print_exc()
        res = None

    end = datetime.now()
    data.addResponse(serviceID, begin, end)
    return jsonify(res)


@app.route('/model/<int:modelID>/service/<int:serviceID>/task', methods=['GET'])
def getAllTasks(modelID, serviceID):
    print('Getting all tasks of model {} service {}'.format(modelID, serviceID))
    begin = datetime.now()

    try:
        records = services.get(serviceID).getTasks()
        res = {'tasks': list(records)}

    except:
        traceback.print_exc()
        res = {'tasks': []}

    end = datetime.now()
    data.addResponse(serviceID, begin, end)
    return jsonify(res)


@app.route('/model/<int:modelID>/service/<int:serviceID>/task/<int:taskID>', methods=['GET'])
def getTaskInfo(modelID, serviceID, taskID):
    print('Getting task {}'.format(taskID))
    begin = datetime.now()

    try:
        service = services.get(serviceID)
        res = {'status': service.getTaskStatus(taskID)}

        if res['status'] == 'finished':
            res['result'] = service.getResult(taskID)
    except:
        traceback.print_exc()
        res = None

    end = datetime.now()
    data.addResponse(serviceID, begin, end)
    return jsonify(res)

# View functions end


if __name__ == '__main__':
    if not os.path.exists('./models'):
        os.makedirs('./models')
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
    # app.run('0.0.0.0', port=5000, debug=True)
