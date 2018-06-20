from modelhublib.model import ModelBase


class Model(ModelBase):

    def __init__(self):
        pass    

    def infer(self, input):
        # Return a constant classification result no matter what's the input
        output = [{"label": "class_0", 'probability': 0.3},
                  {"label": "class_1", 'probability': 0.7}]
        return output
        

class ModelThrowingError(ModelBase):

    def __init__(self):
        pass    

    def infer(self, input):
        raise NotImplementedError

