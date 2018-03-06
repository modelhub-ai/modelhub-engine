from modelhublib.preprocessor import ImagePreprocessorBase
import PIL
import SimpleITK
import numpy as np


class ImagePreprocessor(ImagePreprocessorBase):

    def _preprocessBeforeConvert(self, image):
        if isinstance(image, PIL.Image.Image):
            image = image.resize((224,224), resample = PIL.Image.LANCZOS)
        elif isinstance(image, SimpleITK.Image):
            referenceImage = SimpleITK.Image([224,224], image.GetPixelIDValue())
            image = SimpleITK.Resample(image, referenceImage)
        else:
            raise IOError("Image Type not supported for preprocessing.")
        return image

    def _preprocessAfterConvert(self, npArr):
        if npArr.shape[1] > 3:
            npArr = npArr[:,0:3,:,:]
        elif npArr.shape[1] < 3:
            npArr = npArr[:,[0],:,:]
            npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
            npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
        return npArr
