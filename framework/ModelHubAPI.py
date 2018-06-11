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
        The get_config HTTP method returns the model's config file as a python
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
        The get_legal HTTP method returns the all of modelhub's, the model's,
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
        "model_license", "sample_data_license" ]
        legal = {
            legals[0]:self._get_txt_file("../framework/LICENSE", legals[0]),
            legals[1]:self._get_txt_file("../framework/NOTICE", legals[1]),
            legals[2]:self._get_txt_file("license/model", legals[2]),
            legals[3]:self._get_txt_file("license/sample_data", legals[3])
        }
        return {"legal": legal}

    def get_model_io(self):
        """
        The get_model_io HTTP method is a convinience method that return the
        model's input & output size and type in a python dictionary.
        """
        return {"model_io": self._get_txt_file("model/config.json",
        "config", True)["config"]["model"]["io"]}


    #
    # def get_model_files(self):
    #     '''
    #     The get_model_files HTTP method allows you to download all the model
    #     itself and all its associated files in a single zip folder.
    #
    #     Todo:
    #     * This returns a error: [Errno 32] Broken pipe when url is typed into
    #     chrome and before hitting enter - chrome sends request earlier, and this
    #     messes up with flask.
    #     '''
    #     zip_name = "%s_model"%self.get_txt_file("model/config.json", "config",
    #     True)["config"]["meta"]["name"].lower()
    #     destination_file =  str("%s%s.zip"%(self.working_folder, zip_name))
    #     self.make_archive('../contrib_src/model',destination_file)
    #     return send_file(destination_file, as_attachment=True)
    #
    #

    #
    # def get_sample_urls(self):
    #     '''
    #     This HTTP method
    #     '''
    #     _, _, sample_urls = next(os.walk("sample_data/"))
    #     return jsonify(sample_urls=sample_urls)
