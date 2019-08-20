import unittest
import os
import json

from modelhublib.imageloaders import NumpyImageLoader

class TestNumpyImageLoader(unittest.TestCase):

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testdata"))
        with open(os.path.join(self.testDataDir, "test_config.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.imageLoader = NumpyImageLoader(self.config)

    def tearDown(self):
        pass

    def test_load_numpy_array(self):
        arrayFileName = os.path.join(self.testDataDir, "test_numpy_3x4x4.npy")
        image = self.imageLoader.load(arrayFileName)
        self.assertTupleEqual((3,4,4), image.shape)


if __name__ == '__main__':
    unittest.main()
