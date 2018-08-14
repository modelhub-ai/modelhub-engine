from flask import Flask, jsonify, abort, make_response, send_file, url_for, send_from_directory, request
from .pythonapi import ModelHubAPI
import os
import json
import shutil
from mimetypes import MimeTypes
import requests
from datetime import datetime
# from flask_cors import CORS

class ModelHubRESTAPI:

    def __init__(self, model, contrib_src_dir):
        self.app = Flask(__name__)
        # CORS(self.app)
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
        self.app.add_url_rule('/api/predict_sample', 'predict_sample',
                              self.predict_sample)

    def get_config(self):
        """
        GET method

        Returns:
            application/json: Model configuration dictionary.
        """
        return self._jsonify(self.api.get_config())

    def get_legal(self):
        """
        GET method

        Returns:
            application/json: 
                All of modelhub's, the model's, and the sample data's 
                legal documents as dictionary. If one (or more) of the legal 
                files don't exist, the error  will be logged with the above 
                key. Dictionary keys are:
                    
                - modelhub_license
                - modelhub_acknowledgements
                - model_license
                - sample_data_license
        """
        return self._jsonify(self.api.get_legal())

    def get_model_io(self):
        """
        GET method

        Returns:
            application/json: 
                The model's input/output sizes and types as dictionary.
                Convenience function, as this is a subset of what 
                :func:`~get_config` returns
        """
        return self._jsonify(self.api.get_model_io())

    def get_model_files(self):
        """
        GET method

        Returns:
            application/zip:
                The trained deep learning model in its native format and 
                all its asscociated files in a single zip folder.
        """
        # TODO
        #    * This returns a error: [Errno 32] Broken pipe when url is typed
        #      into chrome and before hitting enter - chrome sends request earlier,
        #      and this messes up with flask.
        #    * Currently no mechanism for catching errors (except what flask
        #      will catch).
        try:
            model_name = self.api.get_config()["meta"]["name"].lower()
            archive_name = os.path.join(self.working_folder, model_name + "_model")
            shutil.make_archive(archive_name, "zip", self.contrib_src_dir, "model")
            return send_file(archive_name + ".zip", as_attachment= True)
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def get_samples(self):
        """
        GET method

        Returns:
            application/json:
                List of URLs to all sample files associated with the model. 
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
        GET/POST method

        Returns:
            application/json:
                Prediciton result on input data. Return type as specified
                in the model configuration (see :func:`~get_model_io`), and
                wrapped in json. In case of an error, returns a dictionary
                with error info.
        
        GET method

        Args:
            fileurl: URL to input data for prediciton. Input type must match
                     specification in the model configuration (see :func:`~get_model_io`)
                     URL must not contain any arguments and should end with the file 
                     extension.

        POST method

        Args:
            file: Input file with data for prediction. Input type must match
                  specification in the model configuration (see :func:`~get_model_io`)

        POST Example: :code:`curl -i -X POST -F file=@<PATH_TO_FILE> "<URL>"`
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
                    return self._jsonify(self.api.predict(file_name, numpyToList=True))
                else:
                    return self._jsonify({'error': 'Incorrect file type.'})
            # through file upload
            elif request.method == 'POST':
                file = request.files.get('file')
                mime_type = file.content_type
                if str(mime_type) in self._get_allowed_extensions():
                    file_name = self._get_file_name(mime_type)
                    file.save(file_name)
                    return self._jsonify(self.api.predict(file_name, numpyToList=True))
                else:
                    return self._jsonify({'error': 'Incorrect file type.'})
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def predict_sample(self):
        """
        GET method

        Performs prediction on sample data.
        
        .. note:: Currently you cannot use :func:`~predict` for inference 
                  on sample data hosted under the same IP as the model api.
                  This function is a temporary workaround. To be removed 
                  in the future.

        Returns:
            application/json:
                Prediciton result on input data. Return type as specified
                in the model configuration (see :func:`~get_model_io`), and
                wrapped in json. In case of an error, returns a dictionary
                with error info.

        Args:
            filename: File name of the sample data. No folders or URLs.
        """
        try:
            if request.method == 'GET':
                file_name = request.args.get('filename')
                file_name = self.contrib_src_dir + "/sample_data/" + file_name
                mime = MimeTypes()
                result = self.api.predict(file_name, numpyToList=True)
                return self._jsonify(result)
        except Exception as e:
            return self._jsonify({'error': str(e)})

    def start(self):
        """
        Starts the flask app.
        """
        self.app.run(host='0.0.0.0', port=80, threaded=True)

    # -------------------------------------------------------------------------
    # Private helper functions
    # -------------------------------------------------------------------------

    def _jsonify(self, content):
        """
        This helper function wraps the flask jsonify function, and also allows
        for error checking. This is usedfor calls that use the
        api._get_txt_file() function that returns a dict key "error" in case
        the file is not found.

        TODO
        * All errors are returned as 400. Would be better to customize the error
          code based on the actual error.
        """
        response = self._addCORS(jsonify(content))
        # response = jsonify(content)
        if (type(content) is dict) and ("error" in content.keys()):
            response.status_code = 400
        return response

    def _addCORS(self, response):
        """
        Adds CORS rules to a given reponse. Should change to specific IP's later.
        """
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

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
