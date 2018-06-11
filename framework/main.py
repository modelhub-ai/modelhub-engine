import ModelHubAPI
import ModelHubRESTAPI
import netron
import sys
import time
from multiprocessing import Process
import os
import glob


def start(model, startNetron=True):
    # temporary
    _testModelHubAPI(model)
    if startNetron:
        _startWithNetron(model)
    else:
        _startWebservice(model)


def _startWithNetron(model):
    netronProcess = Process(target=_startNetron)
    netronProcess.start()
    _startWebservice(model)
    netronProcess.terminate()


def _startNetron():
    path = '/contrib_src/model/'
    for modelFile in glob.glob( os.path.join(path, 'model.*') ):
        netron.serve_file(modelFile, port=81, host="0.0.0.0")


def _startWebservice(model):
    RESTAPI = ModelHubRESTAPI.ModelHubRESTAPI(model)
    RESTAPI.start()

# temporary tests for ModelHubAPI (python)
def _testModelHubAPI(model):
    API = ModelHubAPI.ModelHubAPI(model)
    _testHelper(API.get_config(), 'get_config')
    _testHelper(API.get_legal(), 'get_legal')
    _testHelper(API.get_model_io(), 'get_model_io')
    _testHelper(API.get_samples(), 'get_samples')

def _testHelper(func, name):
    print "TESTING ", name
    print func
