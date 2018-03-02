import unittest

from modelhublib.imageloaders import ImageLoader


class TestImageLoader(unittest.TestCase):

    def setUp(self):
        self.imageLoader = ImageLoader(None)

    def tearDown(self):
        pass

    def test_class_is_abstract(self):
        self.assertRaises(NotImplementedError, self.imageLoader._load, None)
        self.assertRaises(NotImplementedError, self.imageLoader._checkConfigCompliance, None)


if __name__ == '__main__':
    unittest.main()

