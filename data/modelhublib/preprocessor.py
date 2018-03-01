import numpy as np

from modelhublib.imageloaders import PilImageLoader


class ImagePreprocessorBase(object):
    """
    Base class for image preprocessing. An image preprocessor handles loading input 
    images, converting the images to the appropriate numpy array format required 
    by the model, and optionally modifying the image.
    """
    def __init__(self, config):
        self._config = config
        self._imageLoader = PilImageLoader(self._config)
    

    def load(self, input):
        """
        Load input, preprocesses it and returns a numpy array appropriate to feed 
        into the inference model (4 dimensions: [batchsize, z/color, height, width]).

        There should be no need to overwrite this method in a derived class! 
        Rather overwrite the individual processing steps used in this method!
        """
        image = self._load(input)
        image = self._preprocessBeforeConvert(image)
        npArr = self._convertToNumpy(image)
        npArr = self._preprocessAfterConvert(npArr)
        print ('preprocessing done.')
        return npArr


    def _load(self, input):
        """
        Perform the actual loading of the image.
        
        Return image object which type will be the native image object type of 
        the library/handler used for loading. Hence it might not always be the same.
        """
        image = self._imageLoader.load(input)
        return image
    

    def _preprocessBeforeConvert(self, image):
        """
        Perform preprocessing on the native image object (see _load()).
        
        When overwriting this, make sure to handle the possible types appropriately 
        and throw an IOException if you cannot preprocess a certain type.

        Return image object must be of the same type as input image object.
        """
        return image
    

    def _convertToNumpy(self, image):
        """
        Convert the image object into a corresponding numpy array 
        with 4 dimensions: [batchsize, z/color, height, width].
        
        When overwriting this, make sure to handle the possible image 
        object types appropriately and throw IOException if you cannot 
        preprocess a certain type.
        """
        npArr = np.array(image)
        if npArr.ndim == 2:
            npArr = npArr[np.newaxis,:]
        else:
            npArr = np.moveaxis(npArr, -1, 0)
        npArr = npArr[np.newaxis,:].astype(np.float32)
        return npArr
    

    def _preprocessAfterConvert(self, npArr):
        """
        Perform preprocessing on the numpy array (the result of _convertToNumpy()).

        Return numpy array with 4 dimensions: [batchsize, z/color, height, width].
        """
        return npArr

    
