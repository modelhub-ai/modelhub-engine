from modelhublib.postprocessor import PostprocessorBase
import numpy as np
import collections
import json


class Postprocessor(PostprocessorBase):

    def computeOutput(self, inferenceResults):
        probs = np.squeeze(np.asarray(inferenceResults))
        top5Idx = probs.argsort()[-5:][::-1]
        top5Results = collections.OrderedDict()
        with open("model/labels.json") as jsonFile:
            labels = json.load(jsonFile)
        for idx in top5Idx:
            top5Results[labels[str(idx)]] = probs[idx]
        print ('postprocessing done.')
        return top5Results

