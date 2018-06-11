from flask import Flask, render_template, request, send_from_directory, send_file
from urllib import unquote
from redis import Redis, RedisError
import socket
import pprint
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# new API
from flask import abort, jsonify
import os
import json
import utils
import shutil

g_model = None

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

# returns all acknowledgemnts and licenses.
# @app.route('/get_license', methods=['GET'])
# def get_license():
#     if request.method == 'GET':
#         try:
#             result =  jsonify(
#             license=open("../framework/LICENSE",'r').read(),
#             acknowledgements=open("../framework/NOTICE",'r').read(),
#             model_lic=open("license/model",'r').read(),
#             sample_data_lic=open("license/sample_data",'r').read()
#             )
#         except Exception as e:# ALLOWED_EXTENSIONS = json.load(open("model/config.json"))['model']['input']['format']
#             result = "ERROR: " + str(e)
#         return result

# route for getting predictions via file upload
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file and utils.allowed_file(file.filename):
            # save input
            filename = utils.save_uploaded_file(file, app.config['WORKING_FOLDER'])
            try:
                result = g_model.infer(filename)
                result = utils.sort_result_type(result, app.config['WORKING_FOLDER'], filename)
            except Exception as e:
                result = "ERROR: " + str(e)
            return result
        else:
            return jsonify(type='error',result="File format not supported", input=file.filename)


# WARNING TEMP SOLUTION: route for getting predictions via url - only for our
# sample_data only safely works for our sample data - for other urls, we need
# more GET with "content-type" in header
# https://stackoverflow.com/questions/4776924/how-to-safely-get-the-file-extension-from-a-url
@app.route('/predict_sample', methods=['GET'])
def predict_sample():
    if request.method == 'GET':
        filename = request.args.get('filename')
        try:
            result = g_model.infer("sample_data/" + filename)
            result = utils.sort_result_type(result, app.config['WORKING_FOLDER'], "sample_data/" + filename)
        except Exception as e:
            result = "ERROR: " + str(e)
        return result

# routing for figures that exist in the contrib_src - model thumbnail
@app.route('/model/figures/<figureName>')
def sendFigureModel(figureName):
    return send_from_directory("model/figures/", figureName)

# routing for figures that exist in the contrib_src - sample_data
@app.route('/sample_data/<figureName>')
def send_figure_sample(figureName):
    return send_from_directory("../contrib_src/sample_data/", figureName)

# routing to get list of files in sample_data
# @app.route('/get_samples')
# def make_tree():
#     _, _, sample_files = next(os.walk("sample_data/"))
#     return jsonify(samples=sample_files)

# routing for figures that exist in the contrib_src - sample_data
@app.route('/working/<figureName>')
def send_working_files(figureName):
    return send_from_directory("../working/", figureName)

def start(model):
    global g_model
    g_model = model
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(host='0.0.0.0', port=80, threaded=True)
