from flask import Flask, jsonify
import utils


class ModelHubAPI:

    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/api/v1.0/get_config', 'get_config', self.get_config)

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
        return jsonify(utils.get_txt_file("model/config.json", "config", True))

    def start(self):
        # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
        self.app.run(host='0.0.0.0', port=80, threaded=True)
