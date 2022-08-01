import time
import joblib
from pypmml import Model


class Model:
    def pmmlInit(self, file):
        # TODO
        # self.model = xxx
        # self.algo = xxx
        # self.input = xxx
        # self.output = xxx
        self.model = Model.fromFile(file)
        self.algo = self.model.algorithmName
        self.input = []
        self.output = []
        for i in range(0, len(self.model.inputNames)):
            self.input.append({
                'name': 'feature{}'.format(i+1),
                'type': 'double',
                'measure': 'continuous',
                'value': 'any',
            })
        if hasattr(self.model, 'inputNames'):
            for i in range(0, len(self.model.inputNames)):
                self.input[i]['name'] = self.model.inputNames[i]

        if  len(self.model.classes) and not 'float' in [type(x) for x in self.model.classes]:
            output_type = 'integer'
            output_measure = 'nominal'
            output_value = self.model.classes
        elif len(self.model.classes):
            output_type = 'double'
            output_measure = 'nominal'
            output_value = self.model.classes
        else:
            output_type = 'double'
            output_measure = 'continuous'
            output_value = 'any'

        if not self.model.classes.empty()

        for i in range(0, len(self.model.targetNames)):
            self.output.append({
                'name': self.model.targetNames[i],
                'type': output_type,
                'measure': output_measure,
                'value': output_value
            })
        pass

    def onnxInit(self, file):
        # TODO
        # self.model = xxx
        # self.algo = xxx
        # self.input = xxx
        # self.output = xxx
        pass

    def pklInit(self, file):
        self.model = joblib.load(file)
        self.algo = self.model.__class__.__name__
        self.input = []
        self.output = []

        # initial Input
        inputFeatures = self.model.n_features_in_
        for i in range(1, inputFeatures + 1):
            self.input.append({
                'name': 'feature{}'.format(i),
                'type': 'double',
                'measure': 'continuous',
                'value': 'any'
            })

        # if Input has their name...
        if hasattr(self.model, 'feature_names_in_'):
            for i in range(0, inputFeatures):
                self.input[i]['name'] = self.model.feature_names_in_[i]

        self.output.append({
            'name': 'output',
            'type': 'any',
            'measure': 'any',
            'value': 'any'
        })
        pass

    def __init__(self, id, des, type, file):
        self.id = id
        self.des = des
        self.type = type
        self.time = time.time()
        self.count = 0
        self.status = "stop"

        if self.type == "pmml":
            self.pmmlInit(file)
        elif self.type == "onnx":
            self.onnxInit(file)
        elif self.type == "pkl":
            self.pklInit(file)

    def predict(self, x_test):
        return self.model.predict(x_test)


# models dictionary, created with two test models
MODELS = {
    'testModel1': Model('testModel1', 'This is a test model.', 'pmml', None),
    'testModel2': Model('testModel2', 'This is another test model.', 'onnx', None)
}
