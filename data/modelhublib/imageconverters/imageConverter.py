class ImageConverter(object):
    """
    Abstract base class for image converters, following chain of responsibility design pattern.
    """
    def __init__(self, sucessor = None):
        self._sucessor = sucessor
    

    def setSucessor(self, sucessor):
        self._sucessor = sucessor


    def convert(self, image):
        """
        Tries to convert image and on fail forwards convert request to next handler
        until sucess or final fail.
        """
        try:
            npArr = self._convert(image)
        except:
            if self._sucessor:
                return self._sucessor.convert()
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
