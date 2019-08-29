import unittest
import os
import SimpleITK as sitk
import json

from modelhublib.imageloaders import SitkImageLoader

class TestSitkImageLoader(unittest.TestCase):

    def setUp(self):
        self.testDataDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testdata"))
        with open(os.path.join(self.testDataDir, "test_config.json")) as jsonFile:
            self.config = json.load(jsonFile)
        self.imageLoader = SitkImageLoader(self.config)

    def tearDown(self):
        pass

    def test_load_testimage_checkers_64x32(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_checkers_64x32.nrrd")
        image = self.imageLoader.load(imgFileName)
        self.assertTupleEqual((64,32), image.GetSize())

    def test_load_testimage_checkers_64x32_fails_on_config_noncompliance(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_checkers_64x32.nrrd")
        self.config["model"]["io"]["input"]["single"]["dim_limits"][0]["min"] = 1
        self.config["model"]["io"]["input"]["single"]["dim_limits"][2]["max"] = 1
        self.assertRaises(IOError, self.imageLoader.load, imgFileName)

    def test_getImageDimensions_returns_correct_dims(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_checkers_64x32.nrrd")
        image = self.imageLoader.load(imgFileName)
        dims = self.imageLoader._getImageDimensions(image)
        self.assertListEqual([1,32,64], dims)

    def test_load_testimage_nifti_91x109x91(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_nifti_91x109x91.nii.gz")
        image = self.imageLoader.load(imgFileName)
        self.assertTupleEqual((91,109,91), image.GetSize())

    def test_getImageDims_returns_correct_dims_for_nifti(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_nifti_91x109x91.nii.gz")
        image = self.imageLoader.load(imgFileName)
        dims = self.imageLoader._getImageDimensions(image)
        self.assertListEqual([91,109,91], dims)

    def test_load_testimage_dicom_256x256(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_dicom_256x256.dcm")
        image = self.imageLoader.load(imgFileName)
        self.assertTupleEqual((256,256,1), image.GetSize())

    def test_getImageDims_returns_correct_dims_for_dicom(self):
        imgFileName = os.path.join(self.testDataDir, "testimage_dicom_256x256.dcm")
        image = self.imageLoader.load(imgFileName)
        dims = self.imageLoader._getImageDimensions(image)
        self.assertListEqual([1,256,256], dims)


if __name__ == '__main__':
    unittest.main()
