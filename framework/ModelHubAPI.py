from flask import Flask, jsonify, abort, make_response, send_file
import os
import json
import shutil

class ModelHubAPI:

    def __init__(self, model):
        self.app = Flask(__name__)
        self.model = model
        self.working_folder = '../working/'
        self.app.add_url_rule('/api/v1.0/get_config', 'get_config',
        self.get_config)
        self.app.add_url_rule('/api/v1.0/get_legal', 'get_legal',
        self.get_legal)
        self.app.add_url_rule('/api/v1.0/get_model_io', 'get_model_io',
        self.get_model_io)
        self.app.add_url_rule('/api/v1.0/get_model_files', 'get_model_files',
        self.get_model_files)
        self.app.add_url_rule('/api/v1.0/get_sample_urls', 'get_sample_urls',
        self.get_sample_urls)

    def get_txt_file(self, file_path, name, is_json=False):
        """
        This helper function returns a json or txt file if it finds it.
        Otherwise, it returns a 404 error with a message.
        """
        if os.path.isfile(file_path):
            if is_json:
                _file = json.load(open(file_path))
            else:
                _file = open(file_path,'r').read()
            return {name:_file}
        else:
            self.api_error(404, 'Unable to find %s file.'%(file_path))

    def api_error(self, code, message):
        """
        This helper functions allows for custom messages to be included with a
        HTTP code.
        """
        return abort(make_response(jsonify(error=message), code))

    def make_archive(self, source, destination):
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

    def get_config(self):
        '''
        The get_config HTTP method returns the model's config file as a json
        object.

        The config files includes 4 main keys:
        - id: Model uuid.
        - meta: High level information about the model.
        - model: Model specifics.
        - publication: Publication specifics.

        Todo:
        * Put sample config file here.
        * Put link to config.json schema when we have it.
        '''
        return jsonify(self.get_txt_file("model/config.json", "config", True))

    def get_legal(self):
        '''
        The get_legal HTTP method returns the all of modelhub's, the model's,
        and the sample data's legal documents as a json object.

        These specifically include:
        - modelhub_license
        - modelhub_acknowledgements
        - model_license
        - sample_data_license
        '''
        legals = ["modelhub_license", "modelhub_acknowledgements",
        "model_license", "sample_data_license" ]
        legal = {
            legals[0]:self.get_txt_file("../framework/LICENSE", legals[0]),
            legals[1]:self.get_txt_file("../framework/NOTICE", legals[1]),
            legals[2]:self.get_txt_file("license/model", legals[2]),
            legals[3]:self.get_txt_file("license/sample_data", legals[3])
        }
        return jsonify(legal=legal)

    def get_model_files(self):
        '''
        The get_model_files HTTP method allows you to download all the model
        itself and all its associated files in a single zip folder.

        Todo:
        * This returns a error: [Errno 32] Broken pipe when url is typed into
        chrome and before hitting enter - chrome sends request earlier, and this
        messes up with flask.
        '''
        zip_name = "%s_model"%self.get_txt_file("model/config.json", "config",
        True)["config"]["model"]["name"].lower()
        destination_file =  str("%s%s.zip"%(self.working_folder, zip_name))
        self.make_archive('../contrib_src/model',destination_file)
        return send_file(destination_file, as_attachment=True)


    def get_model_io(self):
        '''
        The get_model_io HTTP method is a convinience method that return the
        model's input & output size and type.

        '''
        return jsonify(model_io = self.get_txt_file("model/config.json",
        "config", True)["config"]["model"]["io"])

    def get_sample_urls(self):
        '''
        This HTTP method
        '''
        _, _, sample_urls = next(os.walk("sample_data/"))
        return jsonify(sample_urls=sample_urls)

    def start(self):
        self.app.run(host='0.0.0.0', port=80, threaded=True)
