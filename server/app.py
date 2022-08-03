from gevent import pywsgi
from flask import Flask, jsonify, request
from flask_cors import CORS
from requests import request
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


@app.route('/model', methods=['GET'])
def getAllModels():
    res = {}
    res['models'] = []
    for model in list(MODELS.values()):
        # vars : 将python对象转为dict
        res['models'].append(vars(model))
    return jsonify(res)


@app.route('/model', methods=['POST'])
def createModel():
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>', methods=['GET'])
def getModelInfo(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/test', methods=['POST'])
def testModel(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service', methods=['GET'])
def getAllServices(modelID):
    # TODO
    #
    dic = {
        'services': [],
    }
    serdic = {
        'id': request.get_json().get('id'),
        'time': 'xxx',
        'status': 'running',
        'count': 'xxx',
        'averResTime': 'xxx',
        'maxResTime': 'xxx',
        'minResTime': 'xxx',
    }
    dic['services'].append(serdic)
    #
    pass
    return jsonify(dic)


@app.route('/model/<modelID>/service', methods=['POST'])
def createService(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service/<serviceID>', methods=['POST'])
def changeServiceStatus(modelID, serviceID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service/<serviceID>/quick', methods=['POST'])
def quickPredict(modelID, serviceID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service/<serviceID>/task', methods=['POST'])
def batchPredict(modelID, serviceID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service/<serviceID>/task', methods=['GET'])
def getAllTasks(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service/<serviceID>/task/<taskID>', methods=['GET'])
def getTaskInfo(modelID, serviceID, taskID):
    # TODO
    pass
    return jsonify('test!')


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
