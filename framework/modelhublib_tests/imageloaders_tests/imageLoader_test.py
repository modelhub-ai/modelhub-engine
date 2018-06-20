import unittest

from modelhublib.imageloaders import ImageLoader


class TestImageLoader(unittest.TestCase):

    def setUp(self):
        self.imageLoader = ImageLoader(None)

    def tearDown(self):
        pass

    def test_class_is_abstract(self):
        self.assertRaises(NotImplementedError, self.imageLoader._load, None)
        self.assertRaises(NotImplementedError, self.imageLoader._getImageDimensions, None)
        self.assertRaises(NotImplementedError, self.imageLoader._checkConfigCompliance, None)
    
    def test_load_returns_IOError_on_string_input(self):
        self.assertRaises(IOError, self.imageLoader.load, "nonexistent.png")

    def test_load_returns_IOError_on_non_string_input(self):
        self.assertRaises(IOError, self.imageLoader.load, None)


if __name__ == '__main__':
    unittest.main()

