import SimpleITK
import numpy as np

from .imageConverter import ImageConverter


class SitkToNumpyConverter(ImageConverter):
    """
    Converts SimpltITK.Image objects to Numpy
    """

    def _convert(self, image):
        """
        Args:
            image (SimpleITK.Image): Image object to convert.
        
        Returns:
            Input image object converted to numpy array with 4 dimensions [batchsize, z/color, height, width]
        
        Raises:
            IOError if input is not of type SimpleITK.Image or cannot be converted for other reasons.
        """
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

