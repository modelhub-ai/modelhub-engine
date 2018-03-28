# postprocessing.py
# postprocessing of model outputs to some meaningful format
import collections
import json 
import numpy as np


def postprocess(results):
    probs = np.squeeze(np.asarray(results))
    top5Idx = probs.argsort()[-5:][::-1]    
    top5Results = collections.OrderedDict()
    with open("model/labels.json") as jsonFile:
        labels = json.load(jsonFile)
    for idx in top5Idx:
        top5Results[labels[str(idx)]] = probs[idx]
    print ('postprocessing done.')
    return top5Results
