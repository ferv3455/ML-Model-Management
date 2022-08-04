from datetime import datetime
import traceback

from gevent import pywsgi
from flask import Flask, jsonify, request
from flask_cors import CORS

from model import Model
from service import Service, ServiceList
import data


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, supports_credentials=True)

# all active services
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
        params = request.get_json()  # keys: name, des, type, file
        print('Creating model:', params)

        model = Model(**params) # TODO: model initializer: name, des, type, file
        model.save()            # TODO: save the model to ./models/<id>.<type>

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


@app.route('/model/<modelID>', methods=['GET'])
def getModelInfo(modelID):
    model_params = data.getModelByID(modelID)
    res = {'exist': (model_params is not None)}
    print('Searching for model {}: {}'.format(modelID, res['exist']))

    if res['exist']:
        try:
            # TODO: model initializer: load from file (according to id and type)
            model = Model(model_params['name'], 
                          model_params['des'], model_params['type'])
            param_names = ('name', 'des', 'type', 'algo',
                           'time', 'input', 'output')
            res.update({key: getattr(model, key) for key in param_names})
        except:
            traceback.print_exc()

    return jsonify(res)


@app.route('/model/<modelID>/test', methods=['POST'])
def testModel(modelID):
    try:
        input_data = request.get_json()
        print('Testing on model {}: {}'.format(modelID, input_data))
        model_params = data.getModelByID(modelID)
        model = Model(model_params['name'],
                      model_params['des'], model_params['type'])
        result = model.predict(input_data)
        res = {'output': result}
    except:
        traceback.print_exc()
        res = None

    return jsonify(res)


@app.route('/model/<modelID>/service', methods=['GET'])
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


@app.route('/model/<modelID>/service', methods=['POST'])
def createService(modelID):
    try:
        params = request.get_json()  # keys: name
        print('Creating service:', params)
        serviceID = data.addService(
            (modelID, params['name'], datetime.now(), 'on', 0))

        model_params = data.getModelByID(modelID)
        model = Model(model_params['name'],
                      model_params['des'], model_params['type'])
        services.add(serviceID, Service(serviceID, model))
        res = {'status': 'success'}

    except Exception as exc:
        traceback.print_exc()
        res = {
            'status': 'fail',
            'reason': exc
        }
    return jsonify(res)


@app.route('/model/<modelID>/service/<serviceID>', methods=['POST'])
def changeServiceStatus(modelID, serviceID):
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

    return jsonify(res)


@app.route('/model/<modelID>/service/<serviceID>/quick', methods=['POST'])
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


@app.route('/model/<modelID>/service/<serviceID>/task', methods=['POST'])
def batchPredict(modelID, serviceID):
    print('Batch Predict on model {}, service {}'.format(modelID, serviceID))
    begin = datetime.now()

    try:
        service = services.get(serviceID)
        input_data = request.get_json()
        task_id = service.batch(input_data['file'])
        res = {'id': task_id}
    except:
        traceback.print_exc()
        res = None

    end = datetime.now()
    data.addResponse(serviceID, begin, end)
    return jsonify(res)


@app.route('/model/<modelID>/service/<serviceID>/task', methods=['GET'])
def getAllTasks(modelID, serviceID):
    print('Getting all tasks of model {} service {}'.format(modelID, serviceID))
    try:
        records = data.getTasksByService(serviceID)
        param_name = ('id', 'status')
        res = {'tasks': [{key: r[key] for key in param_name} for r in records]}
    except:
        traceback.print_exc()
        res = {'tasks': []}

    return jsonify(res)


@app.route('/model/<modelID>/service/<serviceID>/task/<taskID>', methods=['GET'])
def getTaskInfo(modelID, serviceID, taskID):
    print('Getting task {}'.format(taskID))
    try:
        task = data.getTaskByID(taskID)
        res = {'status': task['status']}

        if res['status'] == 'finished':
            service = services.get(serviceID)
            res['result'] = service.getResult(taskID)
    except:
        traceback.print_exc()
        res = None

    return jsonify(res)

# View functions end


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
    # app.run('0.0.0.0', port=5000, debug=True)
