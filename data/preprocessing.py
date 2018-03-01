from modelhublib.preprocessor import ImagePreprocessorBase
import PIL
import numpy as np


class ImagePreprocessor(ImagePreprocessorBase):

    def _preprocessBeforeConvert(self, image):
        image = image.resize((224,224), resample = PIL.Image.LANCZOS)
        return image

    def _preprocessAfterConvert(self, npArr):
        if npArr.shape[1] > 3:
            npArr = npArr[:,0:3,:,:]
        elif npArr.shape[1] < 3:
            npArr = npArr[:,[0],:,:]
            npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
            npArr = np.concatenate((npArr, npArr[:,[0],:,:]), axis = 1)
        return npArr
