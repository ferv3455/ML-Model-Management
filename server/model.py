import time


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


# models dictionary, created with two test models
MODELS = {
    'testModel1': Model('testModel1', 'This is a test model.', 'pmml', None),
    'testModel2': Model('testModel2', 'This is another test model.', 'onnx', None)
}
