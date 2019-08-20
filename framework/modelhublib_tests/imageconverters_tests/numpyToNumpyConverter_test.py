import unittest
import os
import json
import PIL
import numpy as np

from modelhublib.imageconverters import NumpyToNumpyConverter

class TestNumpyImageConverter(unittest.TestCase):

    def setUp(self):
        self.imageConverter = NumpyToNumpyConverter()

    def tearDown(self):
        pass

    def test_convert_success_on_arr(self):
        baseline = np.asarray([[1,2,3,4],[2,0,0,0],[1,2,3,4]])
        npArr = self.imageConverter.convert(baseline)
        self.assertEqual(baseline.shape, npArr.shape)

    def test_convert_fails_on_image_as_input(self):
        image = PIL.Image.new("RGB", (64,32))
        self.assertRaises(IOError, self.imageConverter.convert, image)

if __name__ == '__main__':
    unittest.main()
