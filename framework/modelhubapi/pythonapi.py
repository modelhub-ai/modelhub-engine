import os
import json
import time
from datetime import datetime

class ModelHubAPI:

    def __init__(self, model, contrib_src_dir):
        self.model = model
        self.contrib_src_dir = contrib_src_dir
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.framework_dir = os.path.normpath(os.path.join(this_dir, ".."))

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
        config_file_path = self.contrib_src_dir + "/model/config.json"
        return self._load_json(config_file_path)

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
        contrib_license_dir = self.contrib_src_dir + "/license"
        legal = self._load_txt_as_dict(self.framework_dir + "/LICENSE", "modelhub_license")
        legal.update(self._load_txt_as_dict(self.framework_dir + "/NOTICE", "modelhub_acknowledgements"))
        legal.update(self._load_txt_as_dict(contrib_license_dir + "/model", "model_license"))
        legal.update(self._load_txt_as_dict(contrib_license_dir + "/sample_data", "sample_data_license"))
        return legal

    def get_model_io(self):
        """
        The get_model_io method is a convinience method that return the
        model's input & output size and type in a python dictionary.
        """
        config_file_path = self.contrib_src_dir + "/model/config.json"
        config = self._load_json(config_file_path)
        if "error" in config:
            return config
        if ("model" in config) and ("io" in config["model"]):
            return config["model"]["io"]
        else:
            return {'error': 'Config file is malformed.'}
        

    def get_samples(self):
        """
        This get_sample_urls method returns a dictionary of sample files. The
        "folder" key contains the absolute folder path in the container and the
        "files" key contains the file names with extensions. Join these
        together to use the sample files. This separation helps the REST API.
        You can use these to test the model out of the box.
        """
        try:
            sample_data_dir = self.contrib_src_dir + "/sample_data"
            _, _, sample_files = next(os.walk(sample_data_dir))
            return  {"folder": sample_data_dir,
                     "files": sample_files} 
        except Exception as e:
            return {'error': repr(e)}

    def predict(self, file_path):
        """
        The predict method preforms an inference on the model using a given
        input. Returns either a json object or numpy array.

        Args:
            file_path (string): Path to file tp run inference on.

        Todo:
            * Output should be a list of outputs - order of which should match
            whatever is in the config file. The return here should be a list as
            well. Global keys: model, processing time, timestamp. Local keys
            specific to each output in the list: output_name, output_type.
            * what other nice to haves with the predict output?
                - input url?
                - input size?
                - how much has input been resized to work with the model?

        """
        try:
            start = time.time()
            output = self.model.infer(file_path)
            end = time.time()
            config = self.get_config()
            return {'output': output,
                    'output_type': config["model"]["io"]["output"][0]["type"], #hardcoded
                    'output_name': config["model"]["io"]["output"][0]["name"], #hardcoded
                    'timestamp': datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"),
                    'processing_time': round(end-start, 3),
                    'model':
                        { "id": config["id"],
                          "name": config["meta"]["name"]
                        }
                    }
        except Exception as e:
            return {'error': repr(e)}


    # -------------------------------------------------------------------------
    # Private helper functions
    # -------------------------------------------------------------------------
    def _load_txt_as_dict(self, file_path, return_key):
        try:
            with open(file_path,'r') as f:
                txt = f.read()
                return {return_key: txt}
        except Exception as e:
            return {'error': str(e)}
    
    def _load_json(self, file_path):
        try:
            with open(file_path) as f:
                loaded_dict = json.load(f)
                return loaded_dict
        except Exception as e:
            return {'error': str(e)}


