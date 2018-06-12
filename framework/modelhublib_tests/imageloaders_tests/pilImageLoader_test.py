import unittest
import os
import PIL
import json

from modelhublib.imageloaders import PilImageLoader

class TestPilImageLoader(unittest.TestCase):

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testdata"))
        with open(os.path.join(self.testDataDir, "test_config.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.imageLoader = PilImageLoader(self.config)

    def tearDown(self):
        pass

    def test_load_testimage_ramp_4x2(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        image = self.imageLoader.load(imgFileName)
        self.assertTupleEqual((4,2), image.size)

    def test_load_testimage_ramp_4x2_fails_on_config_noncompliance(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        self.config["model"]["io"]["input"]["dim_limits"][2]["min"] = 5
        self.assertRaises(IOError, self.imageLoader.load, imgFileName)

    def test_getImageDimensions_returns_correct_dims(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2.png")
        image = self.imageLoader.load(imgFileName)
        dims = self.imageLoader._getImageDimensions(image)
        self.assertListEqual([1,2,4], dims)



if __name__ == '__main__':
    unittest.main()

