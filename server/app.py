from flask import Flask, jsonify
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route


@app.route('/model', methods=['GET'])
def getAllModels():
    pass
    return jsonify('test!')


@app.route('/model', methods=['POST'])
def createModel():
    pass
    return jsonify('test!')


@app.route('/model/<modelID>', methods=['GET'])
def getModelInfo(modelID):
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/test', methods=['POST'])
def testModel(modelID):
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/service', methods=['POST'])
def changeModelStatus(modelID):
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/quick', methods=['POST'])
def quickPredict(modelID):
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/batch', methods=['POST'])
def batchPredict(modelID):
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/batch', methods=['GET'])
def getAllTasks(modelID):
    pass
    return jsonify('test!')


@app.route('/model/<modelID>/predict/batch/<taskID>', methods=['GET'])
def getTaskInfo(modelID, taskID):
    pass
    return jsonify('test!')


if __name__ == '__main__':
    app.run()
