import unittest

from modelhublib.imageconverters import ImageConverter


class TestImageConverter(unittest.TestCase):

    def setUp(self):
        self.imageConverter = ImageConverter(None)

    def tearDown(self):
        pass

    def test_class_is_abstract(self):
        self.assertRaises(NotImplementedError, self.imageConverter._convert, None)


if __name__ == '__main__':
    unittest.main()

