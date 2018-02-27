from PIL import Image
import numpy as np


class ImagePreprocessorBase(object):
    """
    Base class for image preprocessing. An image preprocessor handles loading input 
    images, converting the images to the appropriate numpy array format required 
    by the model, and optionally modifying the image.
    """
    def __init__(self, config):
        self._config = config
    

    def load(self, input):
        """
        Preprocesses the input and returns a numpy array appropriate to feed into
        the inference model.
        """
        image = self._load(input)
        image = self._preprocessBeforeConvert(image)
        npArr = self._convertToNumpy(image)
        npArr = self._preprocessAfterConvert(npArr)
        print ('preprocessing done.')
        return npArr


    def _load(self, input):
        img = Image.open(input)
        self.__checkConfigCompliance(img)
        return img
    

    def _preprocessBeforeConvert(self, image):
        return image
    

    def _convertToNumpy(self, image):
        npArr = np.array(image)
        if npArr.ndim == 2:
            npArr = npArr[np.newaxis,:]
        else:
            npArr = np.moveaxis(npArr, -1, 0)
        npArr = npArr[np.newaxis,:].astype(np.float32)
        return npArr
    

    def _preprocessAfterConvert(self, npArr):
        return npArr

    
    def __checkConfigCompliance(self, image):
        limits = self._config["model"]["input"]["dim_limits"]
        imageDims = [len(image.getbands())]
        imageDims.extend(list(image.size))
        for i in range(3):
            if ((("min" in limits[i]) and (limits[i]["min"] > imageDims[i])) or
                (("max" in limits[i]) and (limits[i]["max"] < imageDims[i]))):
                raise IOError("Image dimensions %s do not comply with input requirements" % str(tuple(imageDims)))
