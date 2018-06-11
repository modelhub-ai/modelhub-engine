from flask import Flask, jsonify, abort, make_response, send_file
import os
import json
import shutil

class ModelHubAPI:

    def __init__(self, model):
        self.model = model

    def _get_txt_file(self, file_path, name, is_json=False):
        """
        This helper function returns a json or txt file if it finds it.
        Otherwise, it returns an error message. It will always return a python
        dictionary.

        Args:
            file_path (string): Path to requested file.
            name (string): Key to be included in the returned dictionary.
            is_json (bool): If the requested file is a json. False by default.

        """
        try:
            if is_json:
                _file = json.load(open(file_path))
            else:
                _file = open(file_path,'r').read()
            return {name: _file}
        except Exception as e:
            return {'error': str(e)}

    def get_config(self):
        """
        The get_config method returns the model's config file as a python
        dictionary.

        The config files includes 4 main keys:
            - id: Model uuid.
            - meta: High level information about the model.
            - model: Model specifics.
            - publication: Publication specifics.

        Todo:
            * Put sample config file here.
            * Put link to config.json schema when we have it.
        """
        return self._get_txt_file("model/config.json", "config", True)

    def get_legal(self):
        """
        The get_legal method returns the all of modelhub's, the model's,
        and the sample data's legal documents as a python dictionary. If one
        (or more) of the four files listed below returns an error, see its
        corresponding key - this error will be registered in its value.

        These specifically include:
            - modelhub_license
            - modelhub_acknowledgements
            - model_license
            - sample_data_license
        """
        legals = ["modelhub_license", "modelhub_acknowledgements",
        "model_license", "sample_data_license"]
        legal = {
            legals[0]:self._get_txt_file("../framework/LICENSE", legals[0]),
            legals[1]:self._get_txt_file("../framework/NOTICE", legals[1]),
            legals[2]:self._get_txt_file("license/model", legals[2]),
            legals[3]:self._get_txt_file("license/sample_data", legals[3])
        }
        return {"legal": legal}

    def get_model_io(self):
        """
        The get_model_io method is a convinience method that return the
        model's input & output size and type in a python dictionary.
        """
        return {"model_io": self._get_txt_file("model/config.json",
        "config", True)["config"]["model"]["io"]}

    def get_samples(self):
        """
        This get_sample_urls method returns a dictionary of sample files. The
        "folder" key contains the absolute folder path in the container and the
        "files" key contains the file names with extensions. Join these
        together to use the sample files. This separation helps the REST API.
        You can use these to test the model out of the box.
        """
        _, _, sample_files = next(os.walk("sample_data/"))
        return {"samples": {"folder": "/contrib_src/sample_data/",
        "files": sample_files} }
