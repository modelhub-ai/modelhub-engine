import unittest
import io
import os
from modelhubapi import ModelHubRESTAPI



class TestAPIBase(unittest.TestCase):
    """
    Defines common functionality for api test cases.

    This mainly defines convenience asserts to avoid duplicating them in
    the actual api test cases (since the difference in the APIs is mostly
    how they are called, but not the actual results we are expecting)
    """

    def setup_self_temp_output_dir(self):
        self.temp_output_dir = os.path.join(self.this_dir, "temp_output_dir")
        if not os.path.exists(self.temp_output_dir):
            os.makedirs(self.temp_output_dir)

    def assert_config_contains_correct_dict(self, config):
        self.assertEqual("MockId", config["id"])
        self.assertEqual("MockNet", config["meta"]["name"])


    def assert_legal_contains_expected_keys(self, legal):
        self.assertNotIn("error", legal)
        keys = sorted(legal)
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
        self.assertEqual("mask", model_io["output"][1]["name"])
        self.assertEqual("mask_image", model_io["output"][1]["type"])


    def assert_predict_contains_expected_mock_prediction(self, result, expectList = False):
        self.assertEqual("class_0", result["output"][0]["prediction"][0]["label"])
        self.assertEqual(0.3, result["output"][0]["prediction"][0]["probability"])
        self.assertEqual("class_1", result["output"][0]["prediction"][1]["label"])
        self.assertEqual(0.7, result["output"][0]["prediction"][1]["probability"])
        if expectList:
            self.assertListEqual([[0,1,1,0],[0,2,2,0]], result["output"][1]["prediction"])
        else:
            self.assertIsInstance(result["output"][1]["prediction"], basestring)

    def assert_predict_contains_expected_mock_meta_info(self, result):
        self.assertEqual("label_list", result["output"][0]["type"])
        self.assertEqual("probabilities", result["output"][0]["name"])
        self.assertListEqual([2], result["output"][0]["shape"])
        self.assertEqual("mask_image", result["output"][1]["type"])
        self.assertEqual("mask", result["output"][1]["name"])
        self.assertListEqual([2,4], result["output"][1]["shape"])
        self.assertEqual("MockId", result["model"]["id"])
        self.assertEqual("MockNet", result["model"]["name"])



class TestRESTAPIBase(TestAPIBase):
    """
    Defines common functionality for rest api test cases
    """

    def setup_self_temp_work_dir(self):
        self.temp_work_dir = os.path.join(self.this_dir, "temp_work_dir")
        if not os.path.exists(self.temp_work_dir):
            os.makedirs(self.temp_work_dir)

    def setup_self_temp_output_dir(self):
        self.temp_output_dir = os.path.join(self.this_dir, "temp_output_dir")
        if not os.path.exists(self.temp_output_dir):
            os.makedirs(self.temp_output_dir)

    def setup_self_test_client(self, model, contrib_src_dir):
        rest_api = ModelHubRESTAPI(model, self.contrib_src_dir)
        rest_api.working_folder = self.temp_work_dir
        rest_api.api.output_folder = self.temp_output_dir
        app = rest_api.app
        app.config["TESTING"] = True
        self.client = app.test_client()


    #--------------------------------------------------------------------------
    # Private helper/convenience functions
    #--------------------------------------------------------------------------
    def _post_predict_request_on_sample_image(self, sample_image_name):
        test_filename = self.contrib_src_dir + "/sample_data/" + sample_image_name
        extension = os.path.splitext(test_filename)[1]
        with open(test_filename, "rb") as f:
            image_data = io.BytesIO(f.read())
        response = self.client.post("/api/predict",
                                    data = {'file': (image_data, 'test_image' + extension)},
                                    content_type = 'multipart/form-data')
        return response



if __name__ == '__main__':
    unittest.main()
