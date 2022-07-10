import time


class Model:
    def pmmlInit(self, file):
        # self.model = xxx
        # self.algo = xxx
        # self.input = xxx
        # self.output = xxx
        pass

    def onnxInit(self, file):
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
        self.stauts = "stop"

        if self.type == "pmml":
            self.pmmlInit(file)
        elif self.type == "onnx":
            self.onnxInit(file)
