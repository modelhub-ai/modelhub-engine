import unittest
import os
import PIL
import json

from modelhublib.preprocessor import ImagePreprocessorBase

class TestImagePreprocessorBase(unittest.TestCase):

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata"))
        with open(os.path.join(self.testDataDir, "test_config.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.preprocessor = ImagePreprocessorBase(self.config)

    def tearDown(self):
        pass

    def test_convertToNumpy_returns_correct_ndim_on_PILImageL(self):
        image = PIL.Image.new("L", (64, 32))
        npArr = self.preprocessor._convertToNumpy(image)
        self.assertEqual(4, npArr.ndim)
        self.assertTupleEqual((1, 1, 32, 64), npArr.shape)

    def test_convertToNumpy_returns_correct_ndim_on_PILImageRGB(self):
        image = PIL.Image.new("RGB", (64, 32))
        npArr = self.preprocessor._convertToNumpy(image)
        self.assertEqual(4, npArr.ndim)
        self.assertTupleEqual((1, 3, 32, 64), npArr.shape)

    def test_load_testimage_ramp_4x2_under_strict_config_dims(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        self.config["model"]["input"]["dim_limits"][1]["min"] = 2
        self.config["model"]["input"]["dim_limits"][1]["max"] = 2
        self.config["model"]["input"]["dim_limits"][2]["min"] = 4
        self.config["model"]["input"]["dim_limits"][2]["max"] = 4
        npArr = self.preprocessor.load(imgFileName)
        self.assertListEqual([[[[50.0,100.0,150.0,200.0],[50.0,100.0,150.0,200.0]]]], npArr.tolist())

    def test_load_testimage_ramp_4x2_fails_on_config_noncompliance(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        self.config["model"]["input"]["dim_limits"][1]["min"] = 3
        self.assertRaises(IOError, self.preprocessor.load, imgFileName)


if __name__ == '__main__':
    unittest.main()

