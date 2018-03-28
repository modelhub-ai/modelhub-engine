from flask import Flask, render_template, request, send_from_directory
from redis import Redis, RedisError
from werkzeug import secure_filename
import json
from json2html import *
import os
import socket
import wtforms as wtf
from inference import infer

# form
class Average(wtf.Form):
    filename   = wtf.FileField(validators=[wtf.validators.InputRequired()])

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

# app and uploads
app = Flask(__name__)
UPLOAD_DIR = '../uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

def handle_request():
    form = Average(request.form)
    filename = None
    result = "upload a file to get results"
    if request.method == 'POST':
        if request.files:
            file = request.files[form.filename.name]
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                try:
                    result = infer(UPLOAD_DIR + filename)
                except Exception as e:
                    result = "ERROR: " + str(e)
    #
    return form,result


@app.route("/", methods=['GET', 'POST'])
def index():
    config_json = json.load(open("model/config.json"))
    title = config_json['publication']['title']
    config = json2html.convert(json =config_json)
    schematic = '<img src="/model/figures/schematic.png" \
                 alt="schematic" width="auto" height="auto">'
    thumbnail = '<img src="/model/figures/thumbnail.png" \
                 alt="thumbnail" width="auto" height="auto">'
    #
    form, result = handle_request()
    #
    return render_template(
        'index.html',
        title=title,
        config=config,
        schematic=schematic,
        thumbnail=thumbnail,
        form=form,
        result=result
    )


@app.route('/model/figures/<figureName>')
def sendFigure(figureName):
    return send_from_directory("../usr_src/model/figures/", figureName)


def start():
    app.run(host='0.0.0.0', port=80)
