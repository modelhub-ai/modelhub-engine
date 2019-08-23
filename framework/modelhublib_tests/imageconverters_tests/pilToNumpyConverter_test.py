import unittest
import os
import PIL
import json
import numpy as np

from modelhublib.imageconverters import PilToNumpyConverter

class TestPilImageConverter(unittest.TestCase):

    def setUp(self):
        self.imageConverter = PilToNumpyConverter()

    def tearDown(self):
        pass

    def test_convert_success_on_PILImageL(self):
        image = PIL.Image.new("L", (64, 32))
        npArr = self.imageConverter.convert(image)
        self.assertEqual(4, npArr.ndim)
        self.assertTupleEqual((1, 1, 32, 64), npArr.shape)

    def test_convert_success_on_PILImageRGB(self):
        image = PIL.Image.new("RGB", (64, 32))
        npArr = self.imageConverter.convert(image)
        self.assertEqual(4, npArr.ndim)
        self.assertTupleEqual((1, 3, 32, 64), npArr.shape)

    def test_convert_fails_on_numpy_as_input(self):
        image = np.array([[1, 2], [3, 4]])
        self.assertRaises(IOError, self.imageConverter.convert, image)



if __name__ == '__main__':
    unittest.main()
