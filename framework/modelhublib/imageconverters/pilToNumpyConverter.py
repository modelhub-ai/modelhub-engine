import PIL
import numpy as np

from .imageConverter import ImageConverter


class PilToNumpyConverter(ImageConverter):
    """
    Converts PIL.Image objects to Numpy
    """

    def _convert(self, image):
        """
        Args:
            image (PIL.Image): Image object to convert.
        
        Returns:
            Input image object converted to numpy array with 4 dimensions [batchsize, z/color, height, width]
        
        Raises:
            IOError if input is not of type PIL.Image or cannot be converted for other reasons.
        """
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

