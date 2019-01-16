import numpy as np
from .imageLoader import ImageLoader


class NumpyImageLoader(ImageLoader):
    """
    Loads .npy, .npz or pickled files through the numpy python library.
    """

    def _load(self, input):
        """
        Loads input using numpy

        Args:
            input (str): Name of the input file to be loaded

        Returns:
            numpy ndarray
        """
        return np.load(input)


    def _getImageDimensions(self, image):
        """
        Args:
            image (ndarray): Image as loaded by :func:`_load`

        Returns:
            Image dimensions from the numpy array
        """
        return image.shape
