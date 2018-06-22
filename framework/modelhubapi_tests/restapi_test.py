from apitestbase import TestAPIBase
import os
import io
from zipfile import ZipFile
import shutil
import json
from modelhubapi import ModelHubRESTAPI
from modelhubapi_tests.mockmodel.contrib_src.inference import Model


class TestModelHubRESTAPI(TestAPIBase):

    def setUp(self):
        model = Model()
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "contrib_src")
        rest_api = ModelHubRESTAPI(model, self.contrib_src_dir)
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
        self.assertEqual(200, response.status_code)


    def test_get_config_returns_correct_dict(self):
        response = self.client.get("/api/get_config")
        config = json.loads(response.get_data())
        self.assert_config_contains_correct_dict(config)

    
    def test_get_legal_returns_expected_keys(self):
        response = self.client.get("/api/get_legal")
        legal = json.loads(response.get_data())
        self.assert_legal_contains_expected_keys(legal)
    

    def test_get_legal_returns_expected_mock_values(self):
        response = self.client.get("/api/get_legal")
        legal = json.loads(response.get_data())
        self.assert_legal_contains_expected_mock_values(legal)
    

    def test_get_model_io_returns_expected_mock_values(self):
        response = self.client.get("/api/get_model_io")
        model_io = json.loads(response.get_data())
        self.assert_model_io_contains_expected_mock_values(model_io)


    def test_get_samples_returns_path_to_mock_samples(self):
        response = self.client.get("/api/get_samples")
        samples = json.loads(response.get_data())
        self.assertListEqual(["http://localhost/api/samples/testimage_ramp_4x2.png"], samples)
    

    def test_samples_routes_correct(self):
        response = self.client.get("/api/samples/testimage_ramp_4x2.png")
        self.assertEqual("image/png", response.content_type)
    

    def test_thumbnail_routes_correct(self):
        response = self.client.get("/api/thumbnail/thumbnail.jpg")
        self.assertEqual("image/jpeg", response.content_type)
    

    def test_get_model_files_returns_zip(self):
        response = self.client.get("/api/get_model_files")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/zip", response.content_type)


    def test_get_model_files_returned_zip_has_mock_content(self):
        response = self.client.get("/api/get_model_files")
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
        response = self._post_predict_request_on_test_image()
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_prediction(result)
    

    def test_predict_by_post_returns_expected_mock_meta_info(self):
        response = self._post_predict_request_on_test_image()
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_meta_info(result)

    
    # TODO this is not so nice yet, test should not require a download from the inet
    # should probably use a mock server for this
    def test_predict_by_url_returns_expected_mock_prediction(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_prediction(result)
    

    # TODO this is not so nice yet, test should not require a download from the inet
    # should probably use a mock server for this
    def test_predict_by_url_returns_expected_mock_meta_info(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        result = json.loads(response.get_data())
        self.assert_predict_contains_expected_mock_meta_info(result)


    #--------------------------------------------------------------------------
    # Private helper/convenience functions
    #--------------------------------------------------------------------------
    def _post_predict_request_on_test_image(self):
        test_filename = self.contrib_src_dir + "/sample_data/testimage_ramp_4x2.png"
        with open(test_filename, "rb") as f:
            image_data = io.BytesIO(f.read())
        response = self.client.post("/api/predict",
                                    data = {'file': (image_data, 'test_image.png')},
                                    content_type = 'multipart/form-data')
        return response



if __name__ == '__main__':
    unittest.main()

