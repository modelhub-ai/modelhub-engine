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
