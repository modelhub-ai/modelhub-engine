import six


class ImageLoader(object):
    """
    Abstract base class for image loaders, following chain of responsibility design pattern.
    """
    def __init__(self, config, sucessor = None):
        self._config = config
        self._sucessor = sucessor

    
    def setSucessor(self, sucessor):
        self._sucessor = sucessor


    def load(self, input):
        """
        Tries to load input and on fail forwards load request to next handler
        until sucess or final fail.
        """
        try:
            image = self._load(input)
        except:
            if self._sucessor:
                return self._sucessor.load()
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

        When overwriting this, make sure to raise IOError if image does
        not comply with config.
        """
        raise NotImplementedError("This is a method of an abstract class.")

