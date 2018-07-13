from flask import Flask, jsonify, abort, make_response, send_file, url_for, send_from_directory, request
from .pythonapi import ModelHubAPI
import os
import json
import shutil
from mimetypes import MimeTypes
import requests
from datetime import datetime

class ModelHubRESTAPI:

    def __init__(self, model, contrib_src_dir):
        self.app = Flask(__name__)
        self.model = model
        self.contrib_src_dir = contrib_src_dir
        self.working_folder = '/working'
        self.api = ModelHubAPI(model, contrib_src_dir)
        # routes
        self.app.add_url_rule('/api/samples/<sample_name>', 'samples',
                              self._samples)
        self.app.add_url_rule('/api/thumbnail/<thumbnail_name>',
                              'thumbnail', self._thumbnail)
        # primary REST API calls
        self.app.add_url_rule('/api/get_config', 'get_config',
                              self.get_config)
        self.app.add_url_rule('/api/get_legal', 'get_legal',
                              self.get_legal)
        self.app.add_url_rule('/api/get_model_io', 'get_model_io',
                              self.get_model_io)
        self.app.add_url_rule('/api/get_model_files', 'get_model_files',
                              self.get_model_files)
        self.app.add_url_rule('/api/get_samples', 'get_samples',
                              self.get_samples)
        self.app.add_url_rule('/api/predict', 'predict',
                              self.predict, methods= ['GET', 'POST'])

    def _jsonify(self, content):
        """
        This helper function wraps the flask jsonify function, and also allows
        for error checking. This is usedfor calls that use the
        api._get_txt_file() function that returns a dict key "error" in case
        the file is not found.

        Todo:
        * All errors are returned as 400. Would be better to customize the error
        code based on the actual error.
        """
        if (type(content) is dict) and ("error" in content.keys()):
            response = jsonify(content)
            response.status_code = 400
            return response
        else:
            return jsonify(content)

    def _samples(self, sample_name):
        """
        Routing function for sample files that exist in contrib_src.
        """
        return send_from_directory(self.contrib_src_dir + "/sample_data/", sample_name)

    def _thumbnail(self, thumbnail_name):
        """
        Routing function for the thumbnail that exists in contrib_src. The
        thumbnail must be named "thumbnail.jpg".
        """
        return send_from_directory(self.contrib_src_dir + "/model/", thumbnail_name)

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

    def _get_allowed_extensions(self):
        return self.api.get_model_io()["input"]["format"]

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
            model_name = self.api.get_config()["meta"]["name"].lower()
            archive_name = os.path.join(self.working_folder, model_name + "_model")
            shutil.make_archive(archive_name, "zip", self.contrib_src_dir, "model")
            return send_file(archive_name + ".zip", as_attachment= True)
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def get_samples(self):
        """
        Calls api.get_samples(). Uses the "files" object and appends the url
        from the request. Returns a list of urls to the sample files. When the
        sample file urls are called, the call goes through _samples which
        handles the routing. If the returned array is empty, then there are no
        sample files for this model i.e. the "sample/data" folder should always
        exist regardless if empty or not.
        """
        try:
            url = request.url
            url = url.replace("api/get_samples", "api/samples/")
            samples = [ url + sample_name
                        for sample_name in self.api.get_samples()["files"]]
            return self._jsonify(samples)
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
            # through URL
            if request.method == 'GET':
                file_url = request.args.get('fileurl')
                mime = MimeTypes()
                mime_type = mime.guess_type(file_url)
                if str(mime_type[0]) in self._get_allowed_extensions() and mime_type[1] == None:
                    # get file and save.
                    r = requests.get(file_url)
                    file_name = self._get_file_name(mime_type[0])
                    with open(file_name, 'wb') as f:
                        f.write(r.content)
                    return self._jsonify(self.api.predict(file_name))
                else:
                    return self._jsonify({'error': 'Incorrect file type.'})
            # through file upload
            elif request.method == 'POST':
                file = request.files.get('file')
                mime_type = file.content_type
                if str(mime_type) in self._get_allowed_extensions():
                    file_name = self._get_file_name(mime_type)
                    file.save(file_name)
                    return self._jsonify(self.api.predict(file_name))
                else:
                    return self._jsonify({'error': 'Incorrect file type.'})
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def start(self):
        """
        Starts the flask app.
        """
        self.app.run(host='0.0.0.0', port=80, threaded=True)
