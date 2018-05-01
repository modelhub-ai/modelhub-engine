import webservice
import netron
import sys
import time
from multiprocessing import Process


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
    netron.serve_file("/usr_src/model/model.onnx", port=81, host="0.0.0.0")


def _startWebservice():
    webservice.start()
