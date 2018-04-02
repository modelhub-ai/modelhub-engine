import unittest

from modelhublib.postprocessor import PostprocessorBase


class TestPostprocessor(unittest.TestCase):

    def setUp(self):
        self.postprocessor = PostprocessorBase(None)

    def tearDown(self):
        pass

    def test_class_is_abstract(self):
        self.assertRaises(NotImplementedError, self.postprocessor.computeOutput, None)


if __name__ == '__main__':
    unittest.main()

