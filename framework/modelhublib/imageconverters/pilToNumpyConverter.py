import PIL
import numpy as np

from .imageConverter import ImageConverter


class PilToNumpyConverter(ImageConverter):
    """
    Converts PIL.Images to Numpy
    """

    def _convert(self, image):
        if isinstance(image, PIL.Image.Image):
            return self.__convertToNumpy(image)
        else:
            raise IOError("Image is not of type \"PIL.Image.Image\".")
    

    def __convertToNumpy(self, image):
        npArr = np.array(image)
        if npArr.ndim == 2:
            npArr = npArr[np.newaxis,:]
        else:
            npArr = np.moveaxis(npArr, -1, 0)
        npArr = npArr[np.newaxis,:].astype(np.float32)
        return npArr

