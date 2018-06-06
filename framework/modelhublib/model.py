class ModelBase(object):
    """
    Base class for contributer models. Currently this is merely an interface 
    definition that all contributer implemented models have to follow.
    """

    def __init__(self):
        pass
    
    def infer(self, input):
        raise NotImplementedError("This is a method of an abstract class.")

