from pythonapi import ModelHubAPI
from restapi import ModelHubRESTAPI
import netron
import sys
import time
from multiprocessing import Process
import os
import glob


def start(model, contribSrcDir, startNetron=True):
    # temporary
    _testModelHubAPI(model, contribSrcDir)
    if startNetron:
        _startWithNetron(model, contribSrcDir)
    else:
        _startWebservice(model, contribSrcDir)


def _startWithNetron(model, contribSrcDir):
    netronProcess = Process(target=_startNetron)
    netronProcess.start()
    _startWebservice(model, contribSrcDir)
    netronProcess.terminate()


def _startNetron():
    path = '/contrib_src/model/'
    for modelFile in glob.glob( os.path.join(path, 'model.*') ):
        netron.serve_file(modelFile, port=81, host="0.0.0.0")


def _startWebservice(model, contribSrcDir):
    restApi = ModelHubRESTAPI(model, contribSrcDir)
    restApi.start()

# temporary tests for ModelHubAPI (python)
def _testModelHubAPI(model, contribSrcDir):
    api = ModelHubAPI(model, contribSrcDir)
    _testHelper(api.get_config(), 'get_config')
    _testHelper(api.get_legal(), 'get_legal')
    _testHelper(api.get_model_io(), 'get_model_io')
    _testHelper(api.get_samples(), 'get_samples')
    _testHelper(api.predict("/contrib_src/sample_data/house.jpg"), 'predict')

def _testHelper(func, name):
    print "TESTING ", name
    print func
