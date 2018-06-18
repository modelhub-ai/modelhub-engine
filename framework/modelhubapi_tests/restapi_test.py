from apitestbase import TestAPIBase
import os
import shutil
import json
from modelhubapi import ModelHubRESTAPI
from modelhubapi_tests.mockmodel.contrib_src.inference import Model


class TestModelHubRESTAPI(TestAPIBase):

    def setUp(self):
        model = Model()
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "contrib_src")
        rest_api = ModelHubRESTAPI(model, contrib_src_dir)
        self.temp_workdir = os.path.join(self.this_dir, "temp_workdir")
        if not os.path.exists(self.temp_workdir):
            os.makedirs(self.temp_workdir)
        rest_api.working_folder = self.temp_workdir
        app = rest_api.app
        app.config["TESTING"] = True
        self.client = app.test_client()
 

    def tearDown(self):
        shutil.rmtree(self.temp_workdir, ignore_errors=True)
        pass
    

    def test_get_config_responds_ok(self):
        response = self.client.get("/api/get_config")
        self.assertEqual(response.status_code, 200)


    def test_get_config_returns_correct_dict(self):
        response = self.client.get("/api/get_config")
        config = json.loads(response.data)
        self.assert_config_contains_correct_dict(config)

    
    def test_get_legal_returns_expected_keys(self):
        response = self.client.get("/api/get_legal")
        legal = json.loads(response.data)
        self.assert_legal_contains_expected_keys(legal)
    

    def test_get_legal_returns_expected_mock_values(self):
        response = self.client.get("/api/get_legal")
        legal = json.loads(response.data)
        self.assert_legal_contains_expected_mock_values(legal)
    

    def test_get_model_io_returns_expected_mock_values(self):
        response = self.client.get("/api/get_model_io")
        model_io = json.loads(response.data)
        self.assert_model_io_contains_expected_mock_values(model_io)


    def test_get_samples_returns_path_to_mock_samples(self):
        response = self.client.get("/api/get_samples")
        samples = json.loads(response.data)
        self.assertListEqual(["http://localhost/api/samples/testimage_ramp_4x2.png"], samples)
    

    def test_samples_routes_correct(self):
        response = self.client.get("/api/samples/testimage_ramp_4x2.png")
        self.assertEqual("image/png", response.content_type)

    
    # TODO this is not nice yet, test should not require a download from the inet
    # need to use a mock file server for this
    def test_predict_returns_expected_mock_prediction(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        result = json.loads(response.data)
        self.assert_predict_contains_expected_mock_prediction(result)
    

    # TODO this is not nice yet, test should not require a download from the inet
    # need to use a mock file server for this
    def test_predict_returns_expected_mock_meta_info(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        result = json.loads(response.data)
        self.assert_predict_contains_expected_mock_meta_info(result)


if __name__ == '__main__':
    unittest.main()

