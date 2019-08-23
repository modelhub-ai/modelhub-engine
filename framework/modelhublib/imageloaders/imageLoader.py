import six


class ImageLoader(object):
    """
    Abstract base class for image loaders, following chain of responsibility design pattern.
    For each image loader you should implement a corresponding image converter using
    :class:`~modelhublib.imageconverters.imageConverter.ImageConverter` as base class.

    Args:
        sucessor (ImageLoader): Next loader in chain to attempt loading the image if this one fails.
    """
    def __init__(self, config, successor = None):
        self._config = config
        self._successor = successor


    def setSuccessor(self, successor):
        """
        Setting the next loader in chain of responsibility.

        Args:
            sucessor (ImageLoader): Next loader in chain to attempt loading the image if this one fails.
        """
        self._successor = successor


    def load(self, input, id=None):
        """
        Tries to load input and on fail forwards load request to next handler
        until success or final fail.

        There should be no need to overwrite this. Overwrite only
        :func:`~_load` to load the image type you want to support and
        let this function as it is to handle the chain of responsibility and errors.

        Args:
            input (str): Name of the input file to be loaded.

        Returns:
            Image object as loaded by :func:`~_load` or a successor load handler.

        Raises:
            IOError if input could not be loaded by any load handler in the chain.
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
        self._checkConfigCompliance(image, id)
        return image


    def _load(self, input):
        """
        Abstract method. Overwrite to implement loading of the input format you want to support.

        When overwriting this, make sure to raise IOError if input cannot
        be loaded.

        Args:
            input (str): Name of the input file to be loaded.

        Returns:
            Should return image object in the native format of the library using to load it.
        """
        raise NotImplementedError("This is a method of an abstract class.")


    def _checkConfigCompliance(self, image, id=None):
        """
        Checks if image complies with configuration.

        There should be no need to overwrite this. Overwrite only
        :func:`~_getImageDimensions`
        to supply the image dims to check against config.

        Args:
            image: Image object as loaded by :func:`~_load`

        Raises:
            IOError if image dimensions do not comply with configuration.
        """
        imageDims = self._getImageDimensions(image)
        if id is None:
            limits = self._config["model"]["io"]["input"]["single"]["dim_limits"]
        else:
            limits = self._config["model"]["io"]["input"][id]["dim_limits"]
        for i in range(3):
            if ((("min" in limits[i]) and (limits[i]["min"] > imageDims[i])) or
                (("max" in limits[i]) and (limits[i]["max"] < imageDims[i]))):
                raise IOError("Image dimensions %s do not comply with input requirements" % str(tuple(imageDims)))



    def _getImageDimensions(self, image):
        """
        Abstract method. Should return the dimensions of the loaded image, should be a 3 tuple (z, y, x).

        Overwrite this in an implementation of this interface. This function
        is used by :func:`~modelhublib.imageloaders.imageLoader.ImageLoader._checkConfigCompliance`.

        Args:
            image: Image object as loaded by :func:`~modelhublib.imageloaders.imageLoader.ImageLoader._load`

        Returns:
            Should return image dimensions of the image object.
        """
        raise NotImplementedError("This is a method of an abstract class.")
