from flask import Flask
from flask import render_template
from redis import Redis, RedisError
import json
from json2html import *
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    config_json = json.load(open("config.json"))
    title = config_json['publication']['title']
    config = json2html.convert(json =config_json)
    schematic = '<img src="/static/schematic.png" alt="schematic" width="50%" \
    height="auto">'
    thumbnail = '<img src="/static/thumbnail.png" alt="thumbnail" width="10%" \
    height="auto">'
    form = '<form action=""> \
      <input type="file" name="pic" accept="image/*"> \
      <input type="submit"> \
    </form>'
    return render_template('index.html',
    title=title,
    config=config,
    schematic=schematic,
    thumbnail=thumbnail,
    form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
