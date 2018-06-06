import unittest

from modelhublib.model import ModelBase

class TestModelBase(unittest.TestCase):

    def setUp(self):
        self.model = ModelBase()

    def tearDown(self):
        pass

    def test_infer_is_abstract(self):
        self.assertRaises(NotImplementedError, self.model.infer, None)



if __name__ == '__main__':
    unittest.main()

