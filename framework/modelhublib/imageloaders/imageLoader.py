import six


class ImageLoader(object):
    """
    Abstract base class for image loaders, following chain of responsibility design pattern.
    """
    def __init__(self, config, successor = None):
        self._config = config
        self._successor = successor


    def setSuccessor(self, successor):
        self._successor = successor


    def load(self, input):
        """
        Tries to load input and on fail forwards load request to next handler
        until sucess or final fail.
        """
        try:
            image = self._load(input)
        except:
            if self._successor:
                return self._successor.load(input)
            else:
                if isinstance(input, six.string_types):
                    raise IOError("Was not able to load the file \"%s\"." % input)
                else:
                    raise IOError("Was not able to load input of type \"%s\"." % type(input).__name__)
        self._checkConfigCompliance(image)
        return image


    def _load(self, input):
        """
        Loads and return the image of given input.

        When overwriting this, make sure to raise IOError if input cannot
        be loaded.
        """
        raise NotImplementedError("This is a method of an abstract class.")


    def _checkConfigCompliance(self, image):
        """
        Check if image complies with configuration.

        There should be no need to overwrite this. Overwrite only
        "_getImageDimensions" to supply the image dims to check against config.
        """
        imageDims = self._getImageDimensions(image)
        limits = self._config["model"]["io"]["input"]["dim_limits"]
        for i in range(3):
            if ((("min" in limits[i]) and (limits[i]["min"] > imageDims[i])) or
                (("max" in limits[i]) and (limits[i]["max"] < imageDims[i]))):
                raise IOError("Image dimensions %s do not comply with input requirements" % str(tuple(imageDims)))



    def _getImageDimensions(self, image):
        """
        Returns the dimensions of the loaded image, should be a 3 tuple (z, y, x).

        Overwrite this in an implementation of this interface. This function
        is used by "_checkConfigCompliance".
        """
        raise NotImplementedError("This is a method of an abstract class.")
