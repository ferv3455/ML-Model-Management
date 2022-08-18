from importlib import import_module
import time
import joblib
from pypmml import Model as PMMLModel
import onnx
from google.protobuf.json_format import MessageToDict
import torch
import pandas as pd
import onnxruntime
import cv2
import numpy as np


class Model:
    def pmmlInit(self, file):
        # TODO
        self.model = PMMLModel.fromFile(file)
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

        if len(self.model.classes) and not 'float' in [type(x) for x in self.model.classes]:
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

        for i in range(0, len(self.model.targetNames)):
            self.output.append({
                'name': self.model.targetNames[i],
                'type': output_type,
                'measure': output_measure,
                'value': output_value
            })
        print(self.input)
        print(self.output)

    def onnxInit(self, file):
        # TODO
        # self.model = onnx.load(file)
        # self.algo = '-'
        # self.input = []
        # self.output = []
        # graph_dict = MessageToDict(self.model.graph)
        #
        # node_dict = graph_dict['node']
        # if 'opType' in node_dict[0].keys():
        #     self.algo = node_dict[0]['opType']
        #
        # input_list = graph_dict['input']
        # for i in range(len(input_list)):
        #     input_dim_list = input_list[i]['type']['tensorType']['shape']['dim']
        #     dim_input = []
        #     for dim in input_dim_list:
        #         if not dim:
        #             dim_input.append('1')
        #         else:
        #             dim_input.append(dim['dimValue'])
        #     dim_input = ', '.join(dim_input)
        #     self.input.append({
        #         'name': input_list[i]['name'],
        #         'type': 'tensor(float) ' + '(' + dim_input + ')',
        #         'measure': '',
        #         'value': '',
        #     })
        #
        # output_list = graph_dict['output']
        # for i in range(len(output_list)):
        #     type = list(output_list[i]['type'].keys())[0]
        #
        #     if type == 'tensorType':
        #         dim_output = []
        #         output_dim_list = output_list[i]['type']['tensorType']['shape']['dim']
        #         for dim in output_dim_list:
        #             if not dim:
        #                 dim_output.append('1')
        #             else:
        #                 dim_output.append(dim['dimValue'])
        #         dim_output = ', '.join(dim_output)
        #     else:
        #         dim_output = ''
        #     self.output.append({
        #         'name': output_list[i]['name'],
        #         'type': type + ' (' + dim_output + ')',
        #         'measure': '',
        #         'value': '',
        #     })
        self.model = onnxruntime.InferenceSession(file)
        self.algo = '-'
        self.input = []
        self.output = []
        graph_dict = MessageToDict(onnx.load(file).graph)
        node_dict = graph_dict['node']
        if 'opType' in node_dict[0].keys():
            self.algo = node_dict[0]['opType']
        input_tensors = self.model.get_inputs()
        for input_tensor in input_tensors:
            self.input.append({
                'name': input_tensor.name,
                'type': input_tensor.type + ' ' + str(input_tensor.shape),
                'measure': '',
                'value': '',
            })
        output_tensors = self.model.get_outputs()
        for output_tensor in output_tensors:
            self.output.append({
                'name': output_tensor.name,
                'type': output_tensor.type + ' ' + str(output_tensor.shape),
                'measure': '',
                'value': '',
            })
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

    def pthInit(self, file):
        # Has some problems
        self.model = torch.load(file)
        self.algo = 'Neural Networks'
        self.input = []
        self.output = []

        # initial output to find number of classes
        state_dict = self.model['state_dict']
        net_len = len(state_dict)
        state_keys = list(state_dict.keys())
        num_classes = list(state_dict[state_keys[net_len - 1]].size())[0]

        self.output.append({
            'name': 'output',
            'type': 'weight list',
            'measure': 'any',
            'value': str(num_classes)
        })

        # initial input, but can't find standard input size from model file pth
        self.input.append({
            'name': 'input',
            'type': '2D Tensor',
            'measure': 'any',
            'value': 'sized'
        })
        pass

    def __init__(self, name, des, type, file):
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
        elif self.type == "pth":
            self.pthInit(file)

    def predict(self, x_test, pre_processer=None):
        if pre_processer is not None:
            pre_pro_module = import_module(
                pre_processer['path'][2:-3].replace('/', '.'))
            for key, value in x_test.items():
                x_test[key] = pre_pro_module.pre_process(value)

        result = []
        if self.type == 'pmml':
            x = pd.DataFrame([x_test])
            result = self.model.predict(x).values.tolist()
        elif self.type == 'onnx':
            output_names = [output.name for output in self.model.get_outputs()]
            result = self.model.run(output_names, x_test)
            result = [tmp.tolist() for tmp in result]
        elif self.type == 'pkl':
            x = pd.DataFrame([x_test])
            result = self.model.predict(x).tolist()
        else:
            pass
        print(result)
        return result


'''
models dictionary, created with two test models
MODELS = {
    'testModel1': Model('testModel1', 'This is a test model.', 'pmml', None),
    'testModel2': Model('testModel2', 'This is another test model.', 'onnx', None)
}
'''
