from flask import Flask, render_template, request, send_from_directory, jsonify, send_file
from urllib import unquote
from redis import Redis, RedisError
import os
import socket
from inference import infer
import pprint
from PIL import Image
import numpy as np
import utils
import json
# from StringIO import StringIO
# from io import BytesIO

# https://stackoverflow.com/questions/25466904/print-raw-http-request-in-flask-or-wsgi
class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, resp):
        errorlog = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errorlog)

        def log_response(status, headers, *args):
            pprint.pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(environ, log_response)

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

# app and uploads
app = Flask(__name__)
# the working folder contains both uploads and predicted images.
app.config['WORKING_FOLDER'] = '../working/'

@app.route("/", methods=['GET', 'POST'])
def index():
    config_json = json.load(open("model/config.json"))
    name = config_json['meta']['name']
    mailto = "mailto:" + config_json['publication']['email']
    return render_template(
        'index.html',
        name=name,
        mailto=mailto,
        meta=config_json['meta'],
        publication=config_json['publication'],
        model=config_json['model'],
        allowed= ', '.join(config_json['model']['input']['format'])
    )

# route for getting predictions via file upload
@app.route('/predict', methods=['POST'])
def upload1():
    if request.method == 'POST':
        file = request.files['file']
        if file and utils.allowed_file(file.filename):
            # save input
            filename = utils.saveUploadedFile(file, app.config['WORKING_FOLDER'])
            try:
                result = infer(filename)
                if isinstance(result, Image.Image):
                    filename = utils.savePredictedImage(result, app.config['WORKING_FOLDER'])
                    result = jsonify(type='image',result=filename)
                else:
                    result = jsonify(result=result)
            except Exception as e:
                result = "ERROR: " + str(e)
            return result

# WARNING: route for getting predictions via url - only for our sample_data
#  only safely works for our sample data - for other urls, we need more
# GET with "content-type" in header
# https://stackoverflow.com/questions/4776924/how-to-safely-get-the-file-extension-from-a-url
#
@app.route('/predict_sample', methods=['GET'])
def upload2():
    if request.method == 'GET':
        filename = request.args.get('filename')
        try:
            result = infer("../contrib_src/sample_data/" + filename)
            if isinstance(result, Image.Image):
                filename = utils.savePredictedImage(result, app.config['WORKING_FOLDER'])
                result = jsonify(type='image',result=filename)
            else:
                result = jsonify(type='probabilities',result=result)
        except Exception as e:
            result = "ERROR: " + str(e)
        return result

# routing for figures that exist in the contrib_src - model thumbnail
@app.route('/model/figures/<figureName>')
def sendFigureModel(figureName):
    return send_from_directory("../contrib_src/model/figures/", figureName)

# routing for figures that exist in the contrib_src - sample_data
@app.route('/sample_data/<figureName>')
def sendFigureSample(figureName):
    return send_from_directory("../contrib_src/sample_data/", figureName)

# routing to get list of files in sample_data
@app.route('/get_samples')
def make_tree():
    return jsonify(samples=os.listdir("../contrib_src/sample_data/"))

# routing for figures that exist in the contrib_src - sample_data
@app.route('/working/<figureName>')
def sendWorkingFiles(figureName):
    return send_from_directory("../working/", figureName)

def start():
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(host='0.0.0.0', port=80, threaded=True)
