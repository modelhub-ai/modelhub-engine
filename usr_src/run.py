import webservice
import netron
import sys

if __name__ == "__main__":
    if sys.argv[1] == "netron":
        netron.serve_file("/usr_src/model/model.onnx", port=81, host="0.0.0.0")
    else:
        webservice.start()
