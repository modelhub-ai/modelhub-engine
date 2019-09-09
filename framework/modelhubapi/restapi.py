from flask import Flask, jsonify, abort, make_response, send_file, url_for, send_from_directory, request
from .pythonapi import ModelHubAPI
import os
import json
import shutil
from mimetypes import MimeTypes
import requests
from datetime import datetime
from flask_cors import CORS
import magic
import collections # for isinstance with dicts
import re # for url matching regex


class ModelHubRESTAPI:

    def __init__(self, model, contrib_src_dir):
        self.app = Flask(__name__)
        CORS(self.app)
        self.model = model
        self.contrib_src_dir = contrib_src_dir
        self.working_folder = '/working'
        self.api = ModelHubAPI(model, contrib_src_dir)
        # routes
        self.app.add_url_rule('/api/samples/<sample_name>', 'samples',
                              self._samples)
        self.app.add_url_rule('/api/thumbnail/<thumbnail_name>',
                              'thumbnail', self._thumbnail)
        self.app.add_url_rule('/api/output/<output_name>', 'output',
                              self._output)
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
                files don't exist, the error  will be logged with the
                corresponding key. Dictionary keys are:

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
                Prediction result on input data. Return type/format as specified
                in the model configuration (see :func:`~get_model_io`), and
                wrapped in json. In case of an error, returns a dictionary
                with error info.

        GET method

        Args:
            fileurl: URL to input data for prediciton. Input type must match
                     specification in the model configuration (see :func:`~get_model_io`)
                     URL must not contain any arguments and should end with the file
                     extension.

        GET Example: :code:`curl -X GET http://localhost:80/api/predict?fileurl=<URL_OF_FILE>`

        POST method

        Args:
            file: Input file with data for prediction. Input type must match
                  specification in the model configuration (see :func:`~get_model_io`)

        POST Example: :code:`curl -i -X POST -F file=@<PATH_TO_FILE> http://localhost:80/api/predict`
        """
        try:
            file_name, mime_type = self._save_file_get_mime_type(request)
            print(file_name)
            print(mime_type)
            print(self._get_allowed_extensions())
            if str(mime_type) in self._get_allowed_extensions():
                file_name = self._check_multi_inputs(file_name)
                print('Calling predict now')
                print('Passing this to predict: ' + file_name)
                result = self._jsonify(self.api.predict(file_name, url_root=request.url_root))
                os.remove(file_name)
                return result
            else:
                return self._jsonify({'error': 'Incorrect file type.' })
        except Exception as e:
            return self._jsonify({'error': str(e)})


    def predict_sample(self):
        """
        GET method

        Performs prediction on sample data.

        .. note:: Currently you cannot use :func:`~predict` for inference
                  on sample data hosted under the same IP as the model API.
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
                if os.path.isfile(file_name):
                    result = self.api.predict(str(file_name), url_root=request.url_root)
                    return self._jsonify(result)
                else:
                    return self._jsonify({'error': 'The given sample file does not exist.' })
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
        response = jsonify(content)
        if (type(content) is dict) and ("error" in content.keys()):
            response.status_code = 400
        return response

    def _check_multi_inputs(self, file_name):
        if file_name.lower().endswith('.json'):
            folder = "/"+str(file_name).split('/')[-2]
            print('Saving to folder: ' + folder)
            print('is json! Load files!')
            input_dict = self.api._load_json(file_name)
            for key, value in input_dict.items():
                print(value)
                if key == "format":
                    continue
                elif self._check_if_url(value["fileurl"]):
                    input_dict[key]["fileurl"] = self._save_input_from_url(value["fileurl"], folder, value["type"])
                else:
                    print("Apparently this is a local path: " + value["fileurl"])
            # check if value is a url
            # if yes, load and save it
            # then replace the dictionary entry with the local path
            # dump back to file
            self.api._write_json(file_name, input_dict)
        return file_name

    def _check_if_url(self, candidate):
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] | \
            [!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', candidate)
        if len(url) == 1:
            return True
        elif len(url) == 0:
            return False
        else:
            raise IOError("Multiple URLs detected in the input!")

    def _save_input_from_url(self, url, folder, type):
        r = requests.get(url)
        file_name = str(url).split('/')[-1]
        # get file extension from mime types
        file_ext = self._modify_mime_types_inv()[type[0]][0]
        now = datetime.now()
        file_path = os.path.join(folder, "%s%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
        file_ext))
        print('File name in save is: ' + file_path)
        # save without file extension
        with open(file_path, 'wb') as f:
            f.write(r.content)
        # add extension
        #file_name_with_extension = os.path.join(folder, file_name)
        #print(file_name_with_extension)
        #os.rename(file_path, file_name_with_extension)
        return file_path


    def _samples(self, sample_name):
        """
        Routing function for sample files that exist in contrib_src.
        """
        return send_from_directory(self.contrib_src_dir + "/sample_data/", sample_name, cache_timeout=-1)

    def _output(self, output_name):
        """
        Routing function for output files that may exist in the output folder.
        """
        return send_from_directory(self.api.output_folder, output_name, cache_timeout=-1)

    def _thumbnail(self, thumbnail_name):
        """
        Routing function for the thumbnail that exists in contrib_src. The
        thumbnail must be named "thumbnail.jpg".
        """
        return send_from_directory(self.contrib_src_dir + "/model/", thumbnail_name, cache_timeout=-1)

    def _get_allowed_extensions(self):
        return self.api.get_model_io()["input"]["format"]

    def _get_file_name(self, mime_type=""):
        """
        This utility function get the current date/time and returns a full path
        to save either an uploaded file or one grabbed through a url. If
        mimetype is provided, it will grab the appropriate extension, If no
        mimetype is provided, it will return the file without an extension.
        """
        now = datetime.now()
        extension = self._modify_mime_types_inv()[mime_type][0] if mime_type != "" else mime_type
        # print(self._modify_mime_types_inv())
        print('Extension passed: ' + extension)
        print('MIME type passed: ' + mime_type)
        file_name = os.path.join(self.working_folder,
                                 "%s%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
                                 extension))
        return file_name

    def _save_file_get_mime_type(self, request):
        """
        This utility checks first if the request method is POST or GET. It then
        saves the file with a unique date/time name but without an extension.
        Finally it uses magic to identify the mime type and change the filename
        to one with the correct extension. Returns both full path file name and
        mime type.
        """
        if request.method == 'GET':
            file_url = request.args.get('fileurl')
            # cache file extension
            file_name_raw = str(file_url).split('/')[-1]
            print('File name is: ' + file_name_raw)
            file_ext_cache = file_name_raw.split(os.extsep, 1)[-1]
            print('Extension is: ' + file_ext_cache)
            r = requests.get(file_url)
            file_name = self._get_file_name()
            print('File name in save is: ' + file_name)
            with open(file_name, 'wb') as f:
                f.write(r.content)
        elif request.method == 'POST':
            file = request.files.get('file')
            # cache file extension
            file_name_raw = str(file).split('/')[-1]
            print('File name is: ' + file_name_raw)
            file_ext_cache = file_name_raw.split(os.extsep, 1)[-1]
            print('Extension is: ' + file_ext_cache)
            file_name = self._get_file_name()
            file.save(file_name)
        #
        _magic = magic.Magic(mime=True)
        print('Loads MIME type from filename: ' + file_name)
        mime_type = _magic.from_file(file_name)
        print('MIME type for save is: ' + mime_type)

        if mime_type == "text/plain" or mime_type == "application/octet-stream":
            types = self._modify_mime_types()
            try:
                mime_type = types["."+file_ext_cache]
            except KeyError as e:
                raise KeyError("The file extension " + e + " is not supported.")

        file_name_with_extension = self._get_file_name(mime_type)
        os.rename(file_name, file_name_with_extension)
        return file_name_with_extension, mime_type

    def _modify_mime_types_inv(self):
        """
        Inverse: returns a dictionary with mime types as keys.

        Because some file extensions are not available in the MimeTypes library,
        this helper function modeifies it on the fly. This houses all the edge
        conditions.
        """
        mime = MimeTypes()
        original_mime_types = mime.types_map_inv[1]
        original_mime_types["application/octet-stream"] = [".npy"]
        original_mime_types["application/nii"] = [".nii"]
        original_mime_types["application/nii-gzip"] = [".nii.gz"]
        original_mime_types["application/nrrd"] = [".nrrd"]
        original_mime_types["application/dicom"] = [".dcm"]
        return original_mime_types

    def _modify_mime_types(self):
        """
        Returns a dictionary with file extensions as keys

        Because some file extensions are not available in the MimeTypes library,
        this helper function modeifies it on the fly. This houses all the edge
        conditions.
        """
        mime = MimeTypes()
        original_mime_types = mime.types_map[1]
        original_mime_types[".npy"] = ["application/octet-stream"]
        original_mime_types[".nii"] = ["application/nii"]
        original_mime_types[".nii.gz"] = ["application/nii-gzip"]
        original_mime_types[".nrrd"] = ["application/nrrd"]
        original_mime_types[".dcm"] = ["application/dicom"]
        return original_mime_types
