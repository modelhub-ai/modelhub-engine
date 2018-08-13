class ImageConverter(object):
    """
    Abstract base class for image converters, following chain of responsibility design pattern.
    For each image loader derived from :class:`~modelhublib.imageloaders.imageLoader.ImageLoader`
    you should implement a corresponding image converter using this as base class.

    Args:
        sucessor (ImageConverter): Next converter in chain to attempt loading the image if this one fails.
    """
    def __init__(self, successor = None):
        self._successor = successor
    

    def setSuccessor(self, successor):
        """
        Setting the next converter in chain of responsibility.

        Args:
            sucessor (ImageConverter): Next converter in chain to attempt loading the image if this one fails.
        """
        self._successor = successor


    def convert(self, image):
        """
        Tries to convert image to numpy and on fail forwards convert request to next handler
        until sucess or final fail.

        There should be no need to overwrite this. Overwrite only
        :func:`~_convert` to convert the image type you want to support and
        let this function as it is to handle the chain of responsibility and errors.
        
        Args:
            image: Image object to convert.
        
        Returns:
            Numpy array as converted by :func:`~_convert` or a successor converter.

        Raises:
            IOError if image could not be converted by any converter in the chain.
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
        Abstract method. Overwrite to implement image conversion to numpy array
        from the image object type you want to support.

        When overwriting this, make sure to raise IOError if image cannot
        be converted.

        Args:
            image: Image object to convert.
        
        Returns:
            Should return image object converted to numpy array with 4 dimensions [batchsize, z/color, height, width]
        """
        raise NotImplementedError("This is a method of an abstract class.")
