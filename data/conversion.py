# conversion.py
# converts inputs (jpeg, nifti, dicom..etc) to numpy
from PIL import Image
import numpy as np

def convert(imgFile):
   img = Image.open(imgFile)
   img = img.resize((224,224))
   npArr = np.array(img)
   print npArr.shape
   npArr = np.moveaxis(npArr, -1, 0)
   npArr = npArr[np.newaxis,:].astype(np.float32)
   print npArr.shape
   return npArr
