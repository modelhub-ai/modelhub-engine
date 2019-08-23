"""
Implementation of several mock models to test the API. Each model has a
slightly different behaviour, which should be properly handled by the API.
Also most models are not fully valid, e.g. they do not comply to the mock
config. This is ok for unit testing, most models are only used for a small
set of specific tests requiring that model's specific behavioural aspect.

These models test absed on the multi input mock model (contrib_src_mi) with
a single output.
"""

import os
import numpy as np
from modelhublib.model import ModelBase

class Model(ModelBase):

    def __init__(self):
        pass

    def infer(self, input):
        pass

class ModelNeedsTwoInputs(ModelBase):
    def _init_(self):
        pass

    def infer(self, input):
        if isinstance(input, dict):
            return [True]
        else:
            raise IOError("Passed file" + input + "is no dictionary!")

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
