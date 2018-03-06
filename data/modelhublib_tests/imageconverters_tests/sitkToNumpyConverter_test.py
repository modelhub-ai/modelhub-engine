import unittest
import os
import SimpleITK as sitk
import json
import numpy as np

from modelhublib.imageconverters import SitkToNumpyConverter

class TestSitkImageConverter(unittest.TestCase):

    def setUp(self):
        self.imageConverter = SitkToNumpyConverter()

    def tearDown(self):
        pass
    
    def test_convert_success_on_Sitk_Image2d(self):
        image = sitk.Image([4,2], sitk.sitkInt8)
        npArr = self.imageConverter.convert(image)
        self.assertEqual(4, npArr.ndim)
        self.assertTupleEqual((1, 1, 2, 4), npArr.shape)
    
    def test_convert_success_on_Sitk_Image3d(self):
        image = sitk.Image([4,2,3], sitk.sitkInt8)
        npArr = self.imageConverter.convert(image)
        self.assertEqual(4, npArr.ndim)
        self.assertTupleEqual((1, 3, 2, 4), npArr.shape)

    def test_convert_fails_on_numpy_as_input(self):
        image = np.array([[1, 2], [3, 4]])
        self.assertRaises(IOError, self.imageConverter.convert, image)



if __name__ == '__main__':
    unittest.main()

