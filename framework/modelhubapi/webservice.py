from .pythonapi import ModelHubAPI
from .restapi import ModelHubRESTAPI
import sys
import time
from multiprocessing import Process
import os
import glob

def start(model, contribSrcDir):
    _startWebservice(model, contribSrcDir)

def _startWebservice(model, contribSrcDir):
    restApi = ModelHubRESTAPI(model, contribSrcDir)
    restApi.start()
