# conversion.py
# converts inputs (jpeg, nifti, dicom..etc) to numpy
from PIL import Image
import numpy as np

def convert(imgFile):
   img = Image.open(imgFile)
   img = img.resize((224,224))
   npArr = np.array(img)
   npArr = np.moveaxis(npArr, -1, 0)
   npArr = npArr[np.newaxis,:]
   return npArr
