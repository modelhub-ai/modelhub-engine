class ImageConverter(object):
    """
    Abstract base class for image converters, following chain of responsibility design pattern.
    """
    def __init__(self, successor = None):
        self._successor = successor
    

    def setSuccessor(self, successor):
        self._successor = successor


    def convert(self, image):
        """
        Tries to convert image and on fail forwards convert request to next handler
        until sucess or final fail.
        """
        try:
            npArr = self._convert(image)
        except:
            if self._successor:
                return self._successor.convert(image)
            else:
                raise IOError("Could not convert image of type \"%s\" to Numpy array." % type(image).__name__)
        return npArr


    def _convert(self, image):
        """
        Returns image converted to Numpy array.

        When overwriting this, make sure to raise IOError if image cannot
        be converted.
        """
        raise NotImplementedError("This is a method of an abstract class.")
