import SimpleITK
import numpy as np

from modelhublib.imageconverters import ImageConverter


class SitkToNumpyConverter(ImageConverter):
    """
    Converts SimpltITK images to Numpy
    """

    def _convert(self, image):
        if isinstance(image, SimpleITK.Image):
            return self.__convertToNumpy(image)
        else:
            raise IOError("Image is not of type \"SimpleITK.Image\".")
    

    def __convertToNumpy(self, image):
        npArr = SimpleITK.GetArrayFromImage(image)
        if npArr.ndim == 2:
            npArr = npArr[np.newaxis,:]
        npArr = npArr[np.newaxis,:].astype(np.float32)
        return npArr

