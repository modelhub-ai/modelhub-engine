from apitestbase import TestRESTAPIBase
import os
import io
from zipfile import ZipFile
import shutil
import json
from modelhubapi_tests.mockmodel.contrib_src.inference import ModelThrowingError


basicTestGetCalls = ["/api/get_config", 
                     "/api/get_legal", 
                     "/api/get_model_io",
                     "/api/get_samples",
                     "/api/get_model_files"]
class MetaTestModelHubRESTAPIHandlingVoidModel(type):
    
    def __new__(mcs, name, bases, dictionary):
        def test_get_call_returns_error(call):
            def test(self):
                response = self.client.get(call)
                result = json.loads(response.get_data())
                self.assertIn("error", result)
            return test

        for call in basicTestGetCalls:
            testName = "test_get%s_returns_error" % call.replace("/", "_")
            dictionary[testName] = test_get_call_returns_error(call)
            
        return type.__new__(mcs, name, bases, dictionary)



class TestModelHubRESTAPIHandlingVoidModel(TestRESTAPIBase):
    __metaclass__ = MetaTestModelHubRESTAPIHandlingVoidModel

    def setUp(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.contrib_src_dir = os.path.join(self.this_dir, "mockmodel", "void_contrib_src")
        self.setup_self_temp_workdir()
        self.setup_self_test_client(ModelThrowingError(), self.contrib_src_dir)
 

    def tearDown(self):
        shutil.rmtree(self.temp_workdir, ignore_errors=True)
        pass
    

    def test_predict_by_get_returns_error(self):
        response = self.client.get("/api/predict?fileurl=https://raw.githubusercontent.com/modelhub-ai/modelhub-docker/master/framework/modelhublib_tests/testdata/testimage_ramp_4x2.png")
        result = json.loads(response.get_data())
        self.assertIn("error", result)
    
