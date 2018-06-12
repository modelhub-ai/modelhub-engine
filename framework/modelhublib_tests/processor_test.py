import unittest
import os
import PIL
import json

from modelhublib.processor import ImageProcessorBase

# The MetaTestImageProcessorBase meta class is used to generate tests
# that have the same test logic but run over different file types. Using
# this metaclass allows us to simply add new file types for test images
# and generate the same tests for them, as for the existing file types, 
# by simply by adding the file extension to the testFileExtensions list.
testFileExtensions = ["png", "nrrd"]
class MetaTestImageProcessorBase(type):
    
    def __new__(mcs, name, bases, dictionary):
        def gen_test_load_testimage_ramp_4x2_under_strict_config_dims(fileExt):
            def test(self):
                imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2." + fileExt)
                self.config["model"]["io"]["input"]["dim_limits"][1]["min"] = 2
                self.config["model"]["io"]["input"]["dim_limits"][1]["max"] = 2
                self.config["model"]["io"]["input"]["dim_limits"][2]["min"] = 4
                self.config["model"]["io"]["input"]["dim_limits"][2]["max"] = 4
                npArr = self.processor.loadAndPreprocess(imgFileName)
                self.assertListEqual([[[[50.0,100.0,150.0,200.0],[50.0,100.0,150.0,200.0]]]], npArr.tolist())
            return test

        def gen_test_load_testimage_ramp_4x2_fails_on_config_noncompliance(fileExt):
            def test(self):
                imgFileName = os.path.join(self.testDataDir, "testimage_ramp_4x2." + fileExt)
                self.config["model"]["io"]["input"]["dim_limits"][1]["min"] = 3
                self.assertRaises(IOError, self.processor.loadAndPreprocess, imgFileName)
            return test

        for fileExt in testFileExtensions:
            testName = "test_load_testimage_ramp_4x2_%s_under_strict_config_dims" % fileExt
            dictionary[testName] = gen_test_load_testimage_ramp_4x2_under_strict_config_dims(fileExt)
            testName = "test_load_testimage_ramp_4x2_%s_fails_on_config_noncompliance" % fileExt
            dictionary[testName] = gen_test_load_testimage_ramp_4x2_fails_on_config_noncompliance(fileExt)
            
        return type.__new__(mcs, name, bases, dictionary)


class TestImageProcessorBase(unittest.TestCase):
    __metaclass__ = MetaTestImageProcessorBase

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "testdata"))
        with open(os.path.join(self.testDataDir, "test_config.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.processor = ImageProcessorBase(self.config)

    def tearDown(self):
        pass

    def test_computeOutput_is_abstract(self):
        self.assertRaises(NotImplementedError, self.processor.computeOutput, None)



if __name__ == '__main__':
    unittest.main()

