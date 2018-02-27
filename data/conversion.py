# conversion.py
# converts inputs (jpeg, nifti, dicom..etc) to numpy
from PIL import Image
import numpy as np

def convert(imgFile):
    img = Image.open(imgFile)
    img = img.resize((224,224))
    npArr = np.array(img)
    if npArr.ndim == 2:
        npArr = npArr[np.newaxis,:]
    else:
        npArr = np.moveaxis(npArr, -1, 0)
    npArr = npArr[np.newaxis,:].astype(np.float32)
    return npArr
