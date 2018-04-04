from flask import Flask, render_template, request, send_from_directory, jsonify
from urllib import unquote
from redis import Redis, RedisError
from werkzeug import secure_filename
import json
from json2html import *
import os
import socket
import wtforms as wtf
from inference import infer
from datetime import datetime
from collections import OrderedDict

# form
class Average(wtf.Form):
    filename   = wtf.FileField(validators=[wtf.validators.InputRequired()])

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

# app and uploads
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '../uploads/'

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            now = datetime.now()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            try:
                result = infer(filename)
            except Exception as e:
                result = "ERROR: " + str(e)
            return jsonify(result=result)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
        model=config_json['model']
    )

# routing for figures that exist in the usr_src
@app.route('/model/figures/<figureName>')
def sendFigure(figureName):
    return send_from_directory("../usr_src/model/figures/", figureName)

def start():
    app.run(host='0.0.0.0', port=80)
