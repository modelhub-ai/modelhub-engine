from apitestbase import TestAPIBase
import os
from modelhubapi import ModelHubAPI
from modelhubapi_tests.mockmodel.contrib_src.inference import Model


class TestModelHubAPI(TestAPIBase):

    def setUp(self):
        model = Model()
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "contrib_src")
        self.api = ModelHubAPI(model, contrib_src_dir)


    def tearDown(self):
        pass


    def test_get_config_returns_no_error(self):
        config = self.api.get_config()
        self.assertNotIn("error", config)


    def test_get_config_returns_correct_dict(self):
        config = self.api.get_config()
        self.assert_config_contains_correct_dict(config)
    

    def test_get_legal_returns_expected_keys(self):
        legal = self.api.get_legal()
        self.assert_legal_contains_expected_keys(legal)
    

    def test_get_legal_returns_expected_mock_values(self):
        legal = self.api.get_legal()
        self.assert_legal_contains_expected_mock_values(legal)
    

    def test_get_model_io_returns_expected_mock_values(self):
        model_io = self.api.get_model_io()
        self.assert_model_io_contains_expected_mock_values(model_io)


    def test_get_samples_returns_path_to_mock_samples(self):
        samples = self.api.get_samples()
        self.assertEqual(self.this_dir + "/mockmodel/contrib_src/sample_data", samples["folder"])
        self.assertListEqual(["testimage_ramp_4x2.png"], samples["files"])

    
    def test_predict_returns_expected_mock_prediction(self):
        result = self.api.predict("MOCK_MODEL_NEEDS_NO_INPUT_FILE")
        self.assert_predict_contains_expected_mock_prediction(result)
    

    def test_predict_returns_expected_mock_meta_info(self):
        result = self.api.predict("MOCK_MODEL_NEEDS_NO_INPUT_FILE")
        self.assert_predict_contains_expected_mock_meta_info(result)





if __name__ == '__main__':
    unittest.main()

