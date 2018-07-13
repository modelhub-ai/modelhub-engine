import os
import io
from zipfile import ZipFile
import shutil
import json
from modelhubapi_tests.mockmodel.contrib_src.inference import Model
from .apitestbase import TestRESTAPIBase


class TestModelHubRESTAPI(TestRESTAPIBase):

    def setUp(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "contrib_src")
        self.setup_self_temp_workdir()
        self.setup_self_test_client(Model(), self.contrib_src_dir)
     

    def tearDown(self):
        shutil.rmtree(self.temp_workdir, ignore_errors=True)
        pass
    

    def test_get_config_returns_correct_dict(self):
        response = self.client.get("/api/get_config")
        self.assertEqual(200, response.status_code)
        config = json.loads(response.get_data())
        self.assert_config_contains_correct_dict(config)

    
    def test_get_legal_returns_expected_keys(self):
        response = self.client.get("/api/get_legal")
        self.assertEqual(200, response.status_code)
        legal = json.loads(response.get_data())
        self.assert_legal_contains_expected_keys(legal)
    

    def test_get_legal_returns_expected_mock_values(self):
        response = self.client.get("/api/get_legal")
        self.assertEqual(200, response.status_code)
        legal = json.loads(response.get_data())
        self.assert_legal_contains_expected_mock_values(legal)
    

    def test_get_model_io_returns_expected_mock_values(self):
        response = self.client.get("/api/get_model_io")
        self.assertEqual(200, response.status_code)
        model_io = json.loads(response.get_data())
        self.assert_model_io_contains_expected_mock_values(model_io)


    def test_get_samples_returns_path_to_mock_samples(self):
        response = self.client.get("/api/get_samples")
        self.assertEqual(200, response.status_code)
        samples = json.loads(response.get_data())
        samples.sort()
        self.assertListEqual(["http://localhost/api/samples/testimage_ramp_4x2.jpg",
                              "http://localhost/api/samples/testimage_ramp_4x2.png"], 
                             samples)
    

    def test_samples_routes_correct(self):
        response = self.client.get("/api/samples/testimage_ramp_4x2.png")
        self.assertEqual(200, response.status_code)
        self.assertEqual("image/png", response.content_type)
    

    def test_thumbnail_routes_correct(self):
        response = self.client.get("/api/thumbnail/thumbnail.jpg")
        self.assertEqual(200, response.status_code)
        self.assertEqual("image/jpeg", response.content_type)
    

    def test_get_model_files_returns_zip(self):
        response = self.client.get("/api/get_model_files")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/zip", response.content_type)


    def test_get_model_files_returned_zip_has_mock_content(self):
        response = self.client.get("/api/get_model_files")
        self.assertEqual(200, response.status_code)
        test_zip_name = self.temp_workdir + "/test_response.zip"
        with open(test_zip_name, "wb") as test_file:
            test_file.write(response.get_data())
        with ZipFile(test_zip_name, "r") as test_zip:
            reference_content = ["model/",
                                 "model/model.txt",
                                 "model/config.json",
                                 "model/thumbnail.jpg"]
            reference_content.sort()
            zip_content = test_zip.namelist()
            zip_content.sort()
            self.assertListEqual(reference_content, zip_content)
            self.assertEqual("EMPTY MOCK MODEL FOR UNIT TESTING", 
                             test_zip.read("model/model.txt"))

    
    def test_predict_by_post_returns_expected_mock_prediction(self):
        response = self._post_predict_request_on_sample_image("testimage_ramp_4x2.png")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_prediction(result)
    

    def test_predict_by_post_returns_expected_mock_meta_info(self):
        response = self._post_predict_request_on_sample_image("testimage_ramp_4x2.png")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_meta_info(result)


    def test_predict_by_post_returns_error_on_unsupported_file_type(self):
        response = self._post_predict_request_on_sample_image("testimage_ramp_4x2.jpg")
        self.assertEqual(400, response.status_code)
        result = json.loads(response.get_data())
        self.assertIn("error", result)
        self.assertIn("Incorrect file type.", result["error"])

    
    # TODO this is not so nice yet, test should not require a download from the inet
    # should probably use a mock server for this
    def test_predict_by_url_returns_expected_mock_prediction(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_prediction(result)
    

    # TODO this is not so nice yet, test should not require a download from the inet
    # should probably use a mock server for this
    def test_predict_by_url_returns_expected_mock_meta_info(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        self.assertEqual(200, response.status_code)
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_meta_info(result)


    # TODO this is not so nice yet, test should not require a download from the inet
    # should probably use a mock server for this
    def test_predict_by_url_returns_error_on_unsupported_file_type(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.jpg")
        self.assertEqual(400, response.status_code)
        result = json.loads(response.get_data())
        self.assertIn("error", result)
        self.assertIn("Incorrect file type.", result["error"])




if __name__ == '__main__':
    unittest.main()

