import onnx
import onnx_caffe2.backend
import numpy as np
from conversion import convert
from preprocessing import preprocess
from postprocessing import postprocess

def infer():
    # load input
    img = np.random.randn(1, 3, 224, 224).astype(np.float32)
    # convert
    arr = convert(img)
    # preprocess
    arr = preprocess(arr)
    # load ONNX model
    model = onnx.load('model/squeezenet.onnx')
    # Run inference with caffe2
    output = onnx_caffe2.backend.run_model(model, [img])
    # postprocess
    output = postprocess(output)
    return output
