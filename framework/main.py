import webservice
import netron
import sys
import time
from multiprocessing import Process
import os
import glob


def start(startNetron=True):
    if startNetron:
        _startWithNetron()
    else:
        _startWebservice()


def _startWithNetron():
    netronProcess = Process(target=_startNetron)
    netronProcess.start()
    _startWebservice()
    netronProcess.terminate()


def _startNetron():
    path = '/contrib_src/model/'
    for modelFile in glob.glob( os.path.join(path, 'model.*') ):
        netron.serve_file(modelFile, port=81, host="0.0.0.0")


def _startWebservice():
    webservice.start()
