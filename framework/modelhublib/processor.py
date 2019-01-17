import numpy as np

from .imageloaders import PilImageLoader, SitkImageLoader, NumpyImageLoader
from .imageconverters import PilToNumpyConverter, SitkToNumpyConverter, NumpyToNumpyConverter


class ImageProcessorBase(object):
    """
    Abstract base class for image pre- and postprocessing, thus handeling all data 
    processing before and after the inference.

    Several methods of this class have to be implemented in a contributed model.
    Follow the "Contribute Your Model to Modelhub" guide for detailed instructions.

    An image processor handles:

    1. Loading of the input image(s).
    2. Converting the loaded images to a numpy array
    3. Preprocessing the image data (either on the image object or on the numpy array)
       After this step the data should be prepared to be directly feed to the inference step.
    4. Processing the inference result and convert it to the expected output format.

    This class already provides loading and conversion of images using PIL and SimpleITK.
    If you need to support image formats which are not covered by those two, you should
    implement an additional :class:`~modelhublib.imageloaders.imageLoader.ImageLoader` and
    :class:`~modelhublib.imageconverters.imageConverter.ImageConverter`. If you do so,
    you will also need to overwrite the constructor (__init__) to instantiate your
    loader and converter and include them in the chain of responsibility. Best practice
    would be to call the original constructor from your derived class and then change
    what you need to change.

    Args:
        config (dict): Model configuration (loaded from model's config.json)
    """
    
    def __init__(self, config):
        self._config = config
        self._imageLoader = PilImageLoader(self._config)
        self._imageLoader.setSuccessor(SitkImageLoader(self._config))
        self._imageLoader._successor.setSuccessor(NumpyImageLoader(self._config))
        self._imageToNumpyConverter = PilToNumpyConverter()
        self._imageToNumpyConverter.setSuccessor(SitkToNumpyConverter())
        self._imageToNumpyConverter._successor.setSuccessor(NumpyToNumpyConverter())

    def loadAndPreprocess(self, input):
        """
        Loads input, preprocesses it and returns a numpy array appropriate to feed 
        into the inference model (4 dimensions: [batchsize, z/color, height, width]).

        There should be no need to overwrite this method in a derived class! 
        Rather overwrite the individual preprocessing steps used by this method!

        Args:
            input (str): Name of the input file to be loaded

        Returns:
            numpy array appropriate to feed into the inference model 
            (4 dimensions: [batchsize, z/color, height, width])
        """
        image = self._load(input)
        image = self._preprocessBeforeConversionToNumpy(image)
        npArr = self._convertToNumpy(image)
        npArr = self._preprocessAfterConversionToNumpy(npArr)
        return npArr


    def computeOutput(self, inferenceResults):
        """
        Abstract method. Overwrite this method to define how to postprocess 
        the inference results computed by the model into a proper output as 
        defined in the model configuration file.

        Args:
            inferenceResults: Results of the inference as computed by the model.
        
        Returns:
            Converted inference results into format as defined in the model configuration. 
        """
        raise NotImplementedError("This is a method of an abstract class.")
    

    def _load(self, input):
        """
        Performs the actual loading of the image.

        There should be no need to overwrite this method in a derived class!
        Rather implement an additional 
        :class:`~modelhublib.imageloaders.imageLoader.ImageLoader` to support
        further image formats. See also documentation of :class:`~ImageProcessorBase`
        above.
        
        Args:
            input (str): Name of the input file to be loaded

        Returns:
            Image object which type will be the native image object type of 
            the library/handler used for loading (default implementation uses PIL or SimpleITK). 
            Hence it might not always be the same.
        """
        image = self._imageLoader.load(input)
        return image
    

    def _preprocessBeforeConversionToNumpy(self, image):
        """
        Perform preprocessing on the loaded image object (see :func:`~modelhublib.processor.ImageProcessorBase._load`).
        
        Overwrite this to implement image preprocessing using the loaded image object.
        If not overwritten, just returns the image object unchanged.

        When overwriting this, make sure to handle the possible types appropriately 
        and throw an IOException if you cannot preprocess a certain type.

        Args:
            image (type = return of :func:`~modelhublib.processor.ImageProcessorBase._load`): Loaded image object

        Returns:
            Image object which must be of the same type as input image object.
        """
        return image
    

    def _convertToNumpy(self, image):
        """
        Converts the image object into a corresponding numpy array 
        with 4 dimensions: [batchsize, z/color, height, width].

        There should be no need to overwrite this method in a derived class!
        Rather implement an additional 
        :class:`~modelhublib.imageconverters.imageConverter.ImageConverter` to support
        further image format conversions. See also documentation of 
        :class:`~ImageProcessorBase` above.

        Args:
            image: (type = return of :func:`~modelhublib.processor.ImageProcessorBase._preprocessBeforeConversionToNumpy`): Loaded and preproceesed image object.

        Returns:
            Representation of the input image as numpy array with 4 dimensions [batchsize, z/color, height, width].
        """
        npArr = self._imageToNumpyConverter.convert(image)
        return npArr
    

    def _preprocessAfterConversionToNumpy(self, npArr):
        """
        Perform preprocessing on the numpy array (the result of _convertToNumpy()).

        Overwrite this to implement preprocessing on the converted numpy array.
        If not overwritten, just returns the input array unchanged.

        Args:
            npArr (numpy array): input data after conversion by :func:`~modelhublib.processor.ImageProcessorBase._convertToNumpy`

        Returns:
            Preprocessed numpy array with 4 dimensions [batchsize, z/color, height, width].
        """
        return npArr

    
