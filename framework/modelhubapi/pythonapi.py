import os
import io
import json
import time
from datetime import datetime
import numpy

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

        TODO
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
        else:
            return config["model"]["io"]


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

    def predict(self, file_path, numpyToList = False):
        """
        The predict method preforms an inference on the model using a given
        input. 

        Args:
            file_path (string): Path to file tp run inference on.
            numpyToList: Indicates if numpy outputs should be converted to
                         standard python lists.
        
        Returns:
            A dictionary with a list of prediction outputs plus some meta 
            information about the prediction processing.
        """
        try:
            start = time.time()
            output = self.model.infer(file_path)
            output = self._correct_output_list_wrapping(output)
            end = time.time()
            config = self.get_config()
            output_list = []
            for i, o in enumerate(output):
                shape = list(o.shape) if isinstance(o, numpy.ndarray) else [len(o)]
                o = o.tolist() if numpyToList and isinstance(o, numpy.ndarray) else o
                output_list.append({
                    'prediction': o,
                    'shape': shape,
                    'type': config["model"]["io"]["output"][i]["type"],
                    'name': config["model"]["io"]["output"][i]["name"],
                })
            return {'output': output_list,
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
            with io.open(file_path, mode='r', encoding='utf-8') as f:
                txt = f.read()
                return {return_key: txt}
        except Exception as e:
            return {'error': str(e)}

    def _load_json(self, file_path):
        try:
            with io.open(file_path, mode='r', encoding='utf-8') as f:
                loaded_dict = json.load(f)
                return loaded_dict
        except Exception as e:
            return {'error': str(e)}
    
    def _correct_output_list_wrapping(self, output):
        if not isinstance(output, list):
            return [output]
        elif isinstance(output[0], dict):
            return [output]
        else:
            return output

