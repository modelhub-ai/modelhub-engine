class PostprocessorBase(object):
    """
    Base class for inference results postprocessing.
    """

    def __init__(self, config):
        self._config = config
    

    def computeOutput(self, inferenceResults):
        """
        Overwrite this method to define how to postprocess the results computed
        by the model into a proper output that can be interpreted and displayed
        by the modelhub framework.

        Currently supported output formats are:
        - OrderedDict of labels (string) mapped to probabilities (float).
        - 2D or 3D numpy array representing a mask (int), classification 
          labels (int), or probability map (float)
        """
        raise NotImplementedError("This is a method of an abstract class.")

