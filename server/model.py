import time
import joblib
# import data


class Model:
    def pmmlInit(self, file):
        # TODO
        # self.model = xxx
        # self.algo = xxx
        # self.input = xxx
        # self.output = xxx
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

    def blankInit(self):
        self.model = None
        self.algo = 'unknown'
        self.input = []
        self.output = []

    def __init__(self, name,  des, type, file):
        self.name = name
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
        else:
            self.blankInit()

    def predict(self, x_test):
        return self.model.predict(x_test)


# models dictionary, created with two test models
MODELS = {
    'testModel1': Model('testModel1', 'This is a test model.', 'pmml', None),
    'testModel2': Model('testModel2', 'This is another test model.', 'onnx', None)
}
