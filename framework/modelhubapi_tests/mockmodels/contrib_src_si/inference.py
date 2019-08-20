"""
Implementation of several mock models to test the API. Each model has a
slightly different behaviour, which should be properly handled by the API.
Also most models are not fully valid, e.g. they do not comply to the mock
config. This is ok for unit testing, most models are only used for a small
set of specific tests requiring that model's specific behavioural aspect.

These models test based on the single input mock model (contrib_src_si) with
multiple outputs.
"""

import os
import numpy as np
from modelhublib.model import ModelBase


class Model(ModelBase):

    def __init__(self):
        pass

    def infer(self, input):
        if os.path.isfile(input):
            # Return a constant classification result no matter what's the input
            label_list = [{"label": "class_0", 'probability': 0.3},
                          {"label": "class_1", 'probability': 0.7}]
            mask = np.asarray([[0,1,1,0],[0,2,2,0]])
            return [label_list, mask]
        else:
            raise IOError("File " + input + " does not exist.")


class ModelReturnsOneNumpyArray(ModelBase):

    def __init__(self):
        pass

    def infer(self, input):
        if os.path.isfile(input):
            # Return a constant classification result no matter what's the input
            mask = np.asarray([[0,1,1,0],[0,2,2,0]])
            return mask
        else:
            raise IOError("File " + input + " does not exist.")


class ModelReturnsListOfOneNumpyArray(ModelReturnsOneNumpyArray):

    def infer(self, input):
        return [super(ModelReturnsListOfOneNumpyArray, self).infer(input)]


class ModelReturnsOneLabelList(ModelBase):

    def __init__(self):
        pass

    def infer(self, input):
        if os.path.isfile(input):
            # Return a constant classification result no matter what's the input
            label_list = [{"label": "class_0", "probability": 0.3},
                          {"label": "class_1", "probability": 0.7}]
            return label_list
        else:
            raise IOError("File " + input + " does not exist.")


class ModelReturnsListOfOneLabelList(ModelReturnsOneLabelList):

    def infer(self, input):
        return [super(ModelReturnsListOfOneLabelList, self).infer(input)]


class ModelThrowingError(ModelBase):

    def __init__(self):
        pass

    def infer(self, input):
        raise NotImplementedError
