from flask import Flask, jsonify, abort, make_response, send_file
import ModelHubAPI
import os
import json
import shutil

class ModelHubRESTAPI:

    def __init__(self, model):
        self.app = Flask(__name__)
        self.model = model
        self.working_folder = '../working/'
        self.api = ModelHubAPI.ModelHubAPI(model)
        self.app.add_url_rule('/api/v1.0/get_config', 'get_config',
        self.get_config)
        self.app.add_url_rule('/api/v1.0/get_legal', 'get_legal',
        self.get_legal)
        self.app.add_url_rule('/api/v1.0/get_model_io', 'get_model_io',
        self.get_model_io)
        self.app.add_url_rule('/api/v1.0/get_model_files', 'get_model_files',
        self.get_model_files)
        # self.app.add_url_rule('/api/v1.0/get_sample_urls', 'get_sample_urls',
        # self.get_sample_urls)

    def _jsonify(self, _dict):
        """
        This helper function wraps the flask jsonify function, and also allows
        for error checking.

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

    def get_config(self):
        '''
        Calls api.get_config().
        '''
        return self._jsonify(self.api.get_config())

    def get_legal(self):
        '''
        Calls api.get_legal().
        '''
        return self._jsonify(self.api.get_legal())

    def get_model_io(self):
        '''
        Calls api.get_model_io().
        '''
        return self._jsonify(self.api.get_model_io())

    def get_model_files(self):
        '''
        The get_model_files HTTP method allows you to download all the model
        itself and all its associated files in a single zip folder.

        Todo:
        * This returns a error: [Errno 32] Broken pipe when url is typed into
        chrome and before hitting enter - chrome sends request earlier, and this
        messes up with flask.
        '''
        zip_name = "%s_model"%self.api._get_txt_file("model/config.json",
        "config", True)["config"]["meta"]["name"].lower()
        destination_file =  str("%s%s.zip"%(self.working_folder, zip_name))
        self._make_archive('../contrib_src/model',destination_file)
        return send_file(destination_file, as_attachment=True)


    # def get_sample_urls(self):
    #     '''
    #     This HTTP method
    #     '''
    #     _, _, sample_urls = next(os.walk("sample_data/"))
    #     return jsonify(sample_urls=sample_urls)

    def start(self):
        self.app.run(host='0.0.0.0', port=80, threaded=True)
