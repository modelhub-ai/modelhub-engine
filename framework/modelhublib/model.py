class ModelBase(object):
    """
    Abstract base class for contributer models. Currently this is merely an interface 
    definition that all contributer implemented models have to follow.
    """

    def __init__(self):
        pass
    
    def infer(self, input):
        """
        Abstract method. Overwrite this method to implement the inference of a model.

        Args:
            input (str): Input file name.
        
        Returns:
            Converted inference results into format as defined in the model configuration.
            Usually should return the result of 
            :func:`\<YourImageProcessor\>.computeOutput<modelhublib.processor.ImageProcessorBase.computeOutput>`
        """
        raise NotImplementedError("This is a method of an abstract class.")

