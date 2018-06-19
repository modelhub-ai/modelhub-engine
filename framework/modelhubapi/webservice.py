from pythonapi import ModelHubAPI
from restapi import ModelHubRESTAPI
import netron
import sys
import time
from multiprocessing import Process
import os
import glob


def start(model, contribSrcDir, startNetron=True):
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



# tests for REST API (through command line - I am mapping 80 to 4000)
# curl -i http://localhost:4000/api/v1.0/get_config
# curl -i http://localhost:4000/api/v1.0/get_legal
# curl -i http://localhost:4000/api/v1.0/get_model_io
# curl -i http://localhost:4000/api/v1.0/get_model_files
# curl -i http://localhost:4000/api/v1.0/get_samples
# curl -i http://localhost:4000/api/v1.0/get_thumbnail
# these are testing on the same image, one through URL and the other through an upload. We can assert the the output from both is identical
# curl -i http://localhost:4000/api/v1.0/predict?fileurl=https://github.com/modelhub-ai/modelhub/raw/master/squeezenet/contrib_src/sample_data/trump.jpg
# curl -i -X POST -F file=@/home/ahmed/Dropbox/DFCI/14_zoo/modelhub/squeezenet/contrib_src/sample_data/trump.jpg "http://localhost:4000/api/v1.0/predict"

