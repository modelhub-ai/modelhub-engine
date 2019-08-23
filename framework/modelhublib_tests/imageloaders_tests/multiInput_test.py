import unittest
import os
import PIL
import json

from modelhublib.imageloaders import PilImageLoader, SitkImageLoader, NumpyImageLoader

class TestMultiImageLoaderPIL(unittest.TestCase):

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testdata"))
        with open(os.path.join(self.testDataDir, "test_config_mi.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.imageLoader = PilImageLoader(self.config)

    def tearDown(self):
        pass

    def test_load_testimage_ramp_4x2(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        image = self.imageLoader.load(imgFileName, id='name')
        self.assertTupleEqual((4,2), image.size)

    def test_load_testimage_ramp_4x2_fails_on_config_noncompliance(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        self.config["model"]["io"]["input"]["name"]["dim_limits"][2]["min"] = 5
        self.assertRaises(IOError, self.imageLoader.load, imgFileName, id='name')

    def test_getImageDimensions_returns_correct_dims(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        image = self.imageLoader.load(imgFileName, id='name')
        dims = self.imageLoader._getImageDimensions(image)
        self.assertListEqual([1,2,4], dims)

class TestMultiImageLoaderSITK(unittest.TestCase):

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testdata"))
        with open(os.path.join(self.testDataDir, "test_config_mi.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.imageLoader = SitkImageLoader(self.config)

    def tearDown(self):
        pass

    def test_load_testimage_checkers_64x32(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_checkers_64x32.nrrd")
        image = self.imageLoader.load(imgFileName, id='name')
        self.assertTupleEqual((64,32), image.GetSize())

    def test_load_testimage_checkers_64x32_fails_on_config_noncompliance(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_checkers_64x32.nrrd")
        self.config["model"]["io"]["input"]["name"]["dim_limits"][0]["min"] = 1
        self.config["model"]["io"]["input"]["name"]["dim_limits"][2]["max"] = 1
        self.assertRaises(IOError, self.imageLoader.load, imgFileName, id='name')

    def test_getImageDimensions_returns_correct_dims(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_checkers_64x32.nrrd")
        image = self.imageLoader.load(imgFileName, id='name')
        dims = self.imageLoader._getImageDimensions(image)
        self.assertListEqual([1,32,64], dims)

class TestMultiImageLoaderNumpy(unittest.TestCase):

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testdata"))
        with open(os.path.join(self.testDataDir, "test_config_mi.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.imageLoader = NumpyImageLoader(self.config)

    def tearDown(self):
        pass

    def test_load_numpy_array(self):
        arrayFileName = os.path.join(self.testDataDir, "test_numpy_3x4x4.npy")
        image = self.imageLoader.load(arrayFileName, id='name')
        self.assertTupleEqual((3,4,4), image.shape)


if __name__ == '__main__':
    unittest.main()
