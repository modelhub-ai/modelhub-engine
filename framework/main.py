import webservice
import netron
import sys
import time
from multiprocessing import Process
import os
import glob


def start(model, startNetron=True):
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
    webservice.start(model)
