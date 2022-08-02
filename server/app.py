from gevent import pywsgi
from flask import Flask, jsonify, request
from flask_cors import CORS
from model import Model, MODELS
import json


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, supports_credentials=True)

# sanity check route


# TODO: It should be full of BUUUUUUGS now
# TODO: Exception Processing

def getModel(modelID):
    filtered_models = filter(lambda m: m.id == modelID, MODELS)
    assert len(filtered_models) <= 1
    return filtered_models[0] if filtered_models else None


def getTask(model, taskID):
    filtered_tasks = filter(
        lambda t: t.id == taskID and t.model == model, TASKS)
    assert len(filtered_tasks) <= 1
    return filtered_tasks[0] if filtered_tasks else None


@app.route('/model', methods=['GET'])
def getAllModels():
    param_names = ('id', 'des', 'type', 'algo', 'time', 'status')
    res = {"models": [{key: getattr(m, key)
                       for key in param_names} for m in MODELS]}
    return jsonify(res)


@app.route('/model', methods=['POST'])
def createModel():
    params = request.get_json()
    MODELS.append(Model(**params))    # TODO: how to add a model to the list
    res = {
        'status': 'fail',
        'reason': params
    }

    return jsonify(res)


@app.route('/model/<modelID>', methods=['GET'])
def getModelInfo(modelID):
    model = getModel(modelID)
    res = {'exist': (model is not None)}
    if res['exist']:
        param_names = ('des', 'type', 'algo', 'time', 'status',
                       'input', 'output', 'count',
                       'averResTime', 'maxResTime', 'minResTime')
        res.update({key: getattr(model, key) for key in param_names})

    return jsonify(res)


@app.route('/model/<modelID>/test', methods=['POST'])
def testModel(modelID):
    input_data = request.get_json()
    model = getModel(modelID)
    result = model.predict(input_data)

    res = {'output': result}
    return jsonify(res)


@app.route('/model/<modelID>/service', methods=['GET'])
def getAllServices(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service/<serviceID>', methods=['POST'])
def changeServiceStatus(modelID, serviceID):
    # TODO
    cmd = request.get_json()
    model = getModel(modelID)

    try:
        model.setStatus(cmd['opr'])
        status = 'success'
    except:
        status = 'fail'

    res = {'status': status}
    return jsonify(res)


@app.route('/model/<modelID>/service/<serviceID>/quick', methods=['POST'])
def quickPredict(modelID, serviceID):
    # TODO
    model = getModel(modelID)
    if model.status != 'start':
        return jsonify(None)                    # TODO: model not available

    input_data = request.get_json()
    result = model.predict(input_data)
    res = {'output': result}
    return jsonify(res)


@app.route('/model/<modelID>/service/<serviceID>/task', methods=['POST'])
def batchPredict(modelID, serviceID):
    # TODO
    params = request.get_json()
    file = params['file']
    model = getModel(modelID)
    if model.status != 'start':
        return jsonify(None)                    # TODO: model not available

    # task = PredictTask(file, model)
    # TASKS.append(task)                # TODO: how to add a task to the list
    # res = {'id': task.id}
    # return jsonify(res)
    return jsonify({'id': 0})


@app.route('/model/<modelID>/service/<serviceID>/task', methods=['POST'])
def batchPredict(modelID, serviceID):
    # model = getModel(modelID)
    # param_names = ('id', 'status')
    # res = {'tasks': [{key: getattr(t, key)
    #   for key in param_names} for t in TASKS if t.model == model]}
    # return jsonify(res)
    return jsonify({'tasks': []})


@app.route('/model/<modelID>/service/<serviceID>/task/<taskID>', methods=['GET'])
def getTaskInfo(modelID, serviceID, taskID):
    # task = getTask(modelID, taskID)
    # res = {'status': task.status}
    # if res['status'] == 'finished':
    # res['result'] = task.result
    # return jsonify(res)
    return jsonify({'status': 'waiting'})


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
