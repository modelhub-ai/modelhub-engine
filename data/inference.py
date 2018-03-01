import onnx
import onnx_caffe2.backend
import numpy as np
import json
from preprocessing import ImagePreprocessor
from postprocessing import postprocess

def infer(inp):
    config_json = json.load(open("config.json"))
    # load preprocessed input
    preprocessor = ImagePreprocessor(config_json)
    arr = preprocessor.load(inp)
    # load ONNX model
    model = onnx.load('model/squeezenet.onnx')
    # Run inference with caffe2
    output = onnx_caffe2.backend.run_model(model, [arr])
    # postprocess
    output = postprocess(output)
    return output
