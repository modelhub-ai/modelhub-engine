from flask import Flask, jsonify, abort, make_response, send_file, url_for, send_from_directory, request
from pythonapi import ModelHubAPI
import os
import json
import shutil
import re
from mimetypes import MimeTypes
import requests
from datetime import datetime

class ModelHubRESTAPI:

    def __init__(self, model, contrib_src_dir):
        self.app = Flask(__name__)
        self.model = model
        self.contrib_src_dir = contrib_src_dir
        self.working_folder = '/working/'
        self.api = ModelHubAPI(model, contrib_src_dir)
        self.allowed_extensions = self.api.get_model_io()["model_io"]["input"]["format"]
        # routes
        self.app.add_url_rule('/api/v1.0/samples/<sample_name>', 'samples',
        self._samples)
        self.app.add_url_rule('/api/v1.0/thumbnail/<thumbnail_name>',
        'thumbnail', self._thumbnail)
        # primary REST API calls
        self.app.add_url_rule('/api/v1.0/get_config', 'get_config',
        self.get_config)
        self.app.add_url_rule('/api/v1.0/get_legal', 'get_legal',
        self.get_legal)
        self.app.add_url_rule('/api/v1.0/get_model_io', 'get_model_io',
        self.get_model_io)
        self.app.add_url_rule('/api/v1.0/get_model_files', 'get_model_files',
        self.get_model_files)
        self.app.add_url_rule('/api/v1.0/get_samples', 'get_samples',
        self.get_samples)
        self.app.add_url_rule('/api/v1.0/get_thumbnail', 'get_thumbnail',
        self.get_thumbnail)
        self.app.add_url_rule('/api/v1.0/predict', 'predict',
        self.predict, methods= ['GET', 'POST'])

    def _jsonify(self, _dict):
        """
        This helper function wraps the flask jsonify function, and also allows
        for error checking. This is usedfor calls that use the
        api._get_txt_file() function that returns a dict key "error" in case
        the file is not found.

        Todo:
        * All errors are returned as 400. Would be better to customize the error
        code based on the actual error.
        """
        if "error" in _dict.keys():
            return jsonify(self._api_error(400, _dict["error"]))
        else:
            return jsonify(_dict)

    def _api_error(self, code, message):
        """
        This helper functions allows for custom messages to be included with a
        HTTP code.
        """
        return abort(make_response(jsonify(error=message), code))

    def _make_archive(self, source, destination):
        """
        Utility function to archive a given folder.
        http://www.seanbehan.com/how-to-use-python-shutil-make_archive-to-zip-up-
        a-directory-recursively-including-the-root-folder/
        """
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)

    def _samples(self, sample_name):
        """
        Routing function for sample files that exist in contrib_src.
        """
        return send_from_directory("/contrib_src/sample_data/", sample_name)

    def _thumbnail(self, thumbnail_name):
        """
        Routing function for the thumbnail that exists in contrib_src.
        """
        return send_from_directory("/contrib_src/model/", thumbnail_name)

    def _get_file_name(self, mime_type):
        """
        This utility function get the current date/time and returns a full path
        to save either an uploaded file or one grabbed through a url.
        """
        now = datetime.now()
        file_name = os.path.join(self.working_folder,
        "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
        mime_type.split("/")[1]))
        return file_name

    def get_config(self):
        """
        Calls api.get_config().
        """
        return self._jsonify(self.api.get_config())

    def get_legal(self):
        """
        Calls api.get_legal().
        """
        return self._jsonify(self.api.get_legal())

    def get_model_io(self):
        """
        Calls api.get_model_io().
        """
        return self._jsonify(self.api.get_model_io())

    def get_model_files(self):
        """
        The get_model_files HTTP method allows you to download all the model
        itself and all its associated files in a single zip folder.

        Todo:
            * This returns a error: [Errno 32] Broken pipe when url is typed
            into chrome and before hitting enter - chrome sends request earlier,
            and this messes up with flask.
            * Currently no mechanism for catching errors (except what flask
            will catch).
        """
        try:
            zip_name = "%s_model"%self.api._get_txt_file("model/config.json",
            "config", True)["config"]["meta"]["name"].lower()
            destination_file =  str("%s%s.zip"%(self.working_folder, zip_name))
            self._make_archive('/contrib_src/model',destination_file)
            return send_file(destination_file, as_attachment= True)
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def get_samples(self):
        """
        Calls api.get_samples(). Uses the "files" object and appends the url
        from the request. Returns a list of urls to the sample files. When the
        sample file urls are called, the call goes through _samples which
        handles the routing. Assumes that there are always at least one sample
        file, which should always be the case.
        """
        try:
            url = re.sub('\get_samples$', '', request.url) + "samples/"
            samples = [ url + sample_name
            for sample_name in self.api.get_samples()["samples"]["files"]]
            return jsonify(samples = samples)
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def get_thumbnail(self):
        """
        The get_thumbnail HTTP method returns a url to the model thumbnail.
        The thumbnail file must be named "thumbnail", and could either be a jpg
        or png.
        """
        try:
            url = re.sub('\get_thumbnail$', '', request.url) + "thumbnail/"
            path = "/contrib_src/model/"
            if os.path.isfile(path + "thumbnail.jpg"):
                thumbnail = "thumbnail.jpg"
            elif os.path.isfile(path + "thumbnail.png"):
                thumbnail = "thumbnail.png"
            return jsonify(thumbnail = url + thumbnail)
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def predict(self):
        """
        GET: This HTTP method grabs the url from the request arguments and
        checks if its type is allowed and if it is zipped. If it passes these
        tests, it is saved in the working folder and inference is carried out
        on it using api.predict(). Url must not contain any arguments and should
        end with the file extension.

        POST: Similar to GET but based on uploaded files.

        Testing POST with curl
        curl -i -X POST -F file=@<PATH_TO_FILE> "<URL>"
        """
        try:
            if request.method == 'GET':
                file_url = request.args.get('fileurl')
                mime = MimeTypes()
                mime_type = mime.guess_type(file_url)
                if str(mime_type[0]) in self.allowed_extensions and \
                mime_type[1] == None:
                    # get file and save.
                    r = requests.get(file_url)
                    file_name = self._get_file_name(mime_type[0])
                    with open(file_name, 'wb') as f:
                        f.write(r.content)
                    return jsonify(self.api.predict(file_name))
                else:
                    return self._jsonify({'error': 'Incorrect file type.'})
            elif request.method == 'POST':
                file = request.files.get('file')
                mime_type = file.content_type
                if str(mime_type) in self.allowed_extensions:
                    file_name = self._get_file_name(mime_type)
                    file.save(file_name)
                    return jsonify(self.api.predict(file_name))
                else:
                    return self._jsonify({'error': 'Incorrect file type.'})
        except Exception as e:
            return self._jsonify({'error': str(e)})


    def start(self):
        """
        Starts the flask app.
        """
        self.app.run(host='0.0.0.0', port=80, threaded=True)
