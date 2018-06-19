import unittest


class TestAPIBase(unittest.TestCase):
    """
    Defines common functionality for api test cases.

    This mainly defines convenience asserts to avoid duplicating them in 
    the actual api test cases (since the difference in the APIs is mostly
    how they are called, but not the actual results we are expecting)
    """

    def assert_config_contains_correct_dict(self, config):
        self.assertEqual("MockId", config["id"])
        self.assertEqual("MockNet", config["meta"]["name"])
    

    def assert_legal_contains_expected_keys(self, legal):
        self.assertTrue("error" not in legal)
        keys = legal.keys()
        keys.sort()
        referenceKeys = ["model_license", 
                         "modelhub_acknowledgements", 
                         "modelhub_license", 
                         "sample_data_license"]
        self.assertListEqual(referenceKeys, keys)
    

    def assert_legal_contains_expected_mock_values(self, legal):
        self.assertEqual("TEST MODEL LICENSE", legal["model_license"])
        self.assertEqual("TEST SAMPLE DATA LICENSE", legal["sample_data_license"])
    

    def assert_model_io_contains_expected_mock_values(self, model_io):
        self.assertListEqual(["image/png"], model_io["input"]["format"])
        self.assertEqual(1, model_io["input"]["dim_limits"][0]["min"])
        self.assertEqual(4, model_io["input"]["dim_limits"][0]["max"])
        self.assertEqual(1, model_io["input"]["dim_limits"][1]["min"])
        self.assertEqual(1, model_io["input"]["dim_limits"][2]["min"])
        self.assertEqual("probabilities", model_io["output"][0]["name"])
        self.assertEqual("label_list", model_io["output"][0]["type"])


    def assert_predict_contains_expected_mock_prediction(self, result):
        self.assertEqual("class_0", result["output"][0]["label"])
        self.assertEqual(0.3, result["output"][0]["probability"])
        self.assertEqual("class_1", result["output"][1]["label"])
        self.assertEqual(0.7, result["output"][1]["probability"])
    

    def assert_predict_contains_expected_mock_meta_info(self, result):
        self.assertEqual("label_list", result["output_type"])
        self.assertEqual("probabilities", result["output_name"])
        self.assertEqual("MockId", result["model"]["id"])
        self.assertEqual("MockNet", result["model"]["name"])


