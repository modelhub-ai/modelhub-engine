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
        try:
            image = self._load(input)
        except:
            if self._sucessor:
                return self._sucessor.load()
            else:
                if isinstance(input, six.string_types):
                    raise IOError("No handler was able to load the file \"%s\"." % input)
                else:
                    raise IOError("No handler was able to load input of type \"%s\"." % type(input).__name__)
        self._checkConfigCompliance(image)
        return image


    def _load(self, input):
        raise NotImplementedError("This is a method of an abstract class.")


    def _checkConfigCompliance(self, image):
        raise NotImplementedError("This is a method of an abstract class.")

