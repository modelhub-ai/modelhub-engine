import numpy as np

from .imageConverter import ImageConverter


class NumpyToNumpyConverter(ImageConverter):
    """
    In order to follow the chain of responsibility design pattern, this class
    is implemented as a pass through class. It returns the given ndarray as it
    is.
    """

    def _convert(self, image):
        """
        Args:
            image (numpy ndarray)

        Returns:
            image (numpy ndarray)

        Raises:
            IOError if input is not of type ndarray or cannot be converted for
            other reasons.
        """
        if isinstance(image, np.ndarray):
            return image
        else:
            raise IOError("Image is not of type \"np.ndarray\".")
