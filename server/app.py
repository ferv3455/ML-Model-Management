from gevent import pywsgi
from flask import Flask, jsonify
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


@app.route('/model/<modelID>/service', methods=['POST'])
def changeModelStatus(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/quick', methods=['POST'])
def quickPredict(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/batch', methods=['POST'])
def batchPredict(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/batch', methods=['GET'])
def getAllTasks(modelID):
    # TODO
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/batch/<taskID>', methods=['GET'])
def getTaskInfo(modelID, taskID):
    # TODO
    pass
    return jsonify('test!')


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
