import unittest
import os
from modelhubapi import ModelHubAPI
from modelhubapi_tests.mockmodel.contrib_src.inference import Model


class TestModelHubAPI(unittest.TestCase):

    def setUp(self):
        model = Model()
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "contrib_src")
        self.api = ModelHubAPI(model, contrib_src_dir)


    def tearDown(self):
        pass


    def test_get_config_returns_no_error(self):
        config = self.api.get_config()
        self.assertTrue("error" not in config)


    def test_get_config_returns_correct_dict(self):
        config = self.api.get_config()
        self.assertEqual("MockId", config["id"])
        self.assertEqual("MockNet", config["meta"]["name"])
    

    def test_get_legal_returns_expected_keys(self):
        legal = self.api.get_legal()
        self.assertTrue("error" not in legal)
        keys = legal.keys()
        keys.sort()
        referenceKeys = ["model_license", 
                         "modelhub_acknowledgements", 
                         "modelhub_license", 
                         "sample_data_license"]
        self.assertListEqual(referenceKeys, keys)
    

    def test_get_legal_returns_expected_mock_values(self):
        legal = self.api.get_legal()
        self.assertEqual("TEST MODEL LICENSE", legal["model_license"])
        self.assertEqual("TEST SAMPLE DATA LICENSE", legal["sample_data_license"])
    

    def test_get_model_io_returns_expected_mock_values(self):
        model_io = self.api.get_model_io()
        self.assertListEqual(["image/png"], model_io["input"]["format"])
        self.assertEqual(1, model_io["input"]["dim_limits"][0]["min"])
        self.assertEqual(4, model_io["input"]["dim_limits"][0]["max"])
        self.assertEqual(1, model_io["input"]["dim_limits"][1]["min"])
        self.assertEqual(1, model_io["input"]["dim_limits"][2]["min"])
        self.assertEqual("probabilities", model_io["output"][0]["name"])
        self.assertEqual("label_list", model_io["output"][0]["type"])


    def test_get_samples_returns_path_to_mock_samples(self):
        samples = self.api.get_samples()
        self.assertEqual(self.this_dir + "/mockmodel/contrib_src/sample_data", samples["folder"])
        self.assertListEqual(["testimage_ramp_4x2.png"], samples["files"])

    
    def test_predict_returns_expected_mock_prediction(self):
        result = self.api.predict("MOCK_MODEL_NEEDS_NO_INPUT_FILE")
        self.assertEqual("class_0", result["output"][0]["label"])
        self.assertEqual(0.3, result["output"][0]["probability"])
        self.assertEqual("class_1", result["output"][1]["label"])
        self.assertEqual(0.7, result["output"][1]["probability"])
    

    def test_predict_returns_expected_mock_meta_info(self):
        result = self.api.predict("MOCK_MODEL_NEEDS_NO_INPUT_FILE")
        self.assertEqual("label_list", result["output_type"])
        self.assertEqual("probabilities", result["output_name"])
        self.assertEqual("MockId", result["model"]["id"])
        self.assertEqual("MockNet", result["model"]["name"])





if __name__ == '__main__':
    unittest.main()

