"""Implements test cases in which smth is wrong with the model setup"""

import os
import io
from zipfile import ZipFile
import shutil
import json
import six
from modelhubapi_tests.mockmodel.contrib_src.inference import ModelThrowingError
from .apitestbase import TestRESTAPIBase


basicTestGetCalls = [("/api/get_config", 400),
                     ("/api/get_legal", 400),
                     ("/api/get_model_io", 400),
                     ("/api/get_samples", 400),
                     ("/api/get_model_files", 400)]
class MetaTestModelHubRESTAPIVoidModel(type):

    def __new__(mcs, name, bases, dictionary):
        def test_get_call_returns_error(call, resp_code):
            def test(self):
                response = self.client.get(call)
                self.assertEqual(resp_code, response.status_code)
                result = json.loads(response.get_data())
                self.assertIn("error", result)
            return test

        for call, resp_code in basicTestGetCalls:
            testName = "test_get%s_returns_error" % call.replace("/", "_")
            dictionary[testName] = test_get_call_returns_error(call, resp_code)

        return type.__new__(mcs, name, bases, dictionary)



@six.add_metaclass(MetaTestModelHubRESTAPIVoidModel)
class TestModelHubRESTAPIVoidModel(TestRESTAPIBase):

    def setUp(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "void_contrib_src")
        self.setup_self_temp_work_dir()
        self.setup_self_temp_output_dir()
        self.setup_self_test_client(ModelThrowingError(), self.contrib_src_dir)


    def tearDown(self):
        shutil.rmtree(self.temp_work_dir, ignore_errors=True)
        shutil.rmtree(self.temp_output_dir, ignore_errors=True)
        pass


    def test_predict_by_get_returns_error(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        self.assertEqual(400, response.status_code)
        result = json.loads(response.get_data())
        self.assertIn("error", result)



class TestModelHubRESTAPIModelThrowingError(TestRESTAPIBase):

    def setUp(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "contrib_src")
        self.setup_self_temp_work_dir()
        self.setup_self_temp_output_dir()
        self.setup_self_test_client(ModelThrowingError(), self.contrib_src_dir)


    def tearDown(self):
        shutil.rmtree(self.temp_work_dir, ignore_errors=True)
        pass


    def test_predict_by_get_returns_exception(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        self.assertEqual(400, response.status_code)
        result = json.loads(response.get_data())
        self.assertIn("error", result)
        self.assertIn("NotImplementedError", result["error"])


    def test_predict_by_post_returns_exception(self):
        response = self._post_predict_request_on_sample_image("testimage_ramp_4x2.png")
        self.assertEqual(400, response.status_code)
        result = json.loads(response.get_data())
        self.assertIn("error", result)
        self.assertIn("NotImplementedError", result["error"])



if __name__ == '__main__':
    unittest.main()
