import os
import io
import json
import time
from datetime import datetime
import numpy

class ModelHubAPI:
    """
    Generic interface to access a model.
    """

    def __init__(self, model, contrib_src_dir):
        self.model = model
        self.output_folder = '/output'
        self.contrib_src_dir = contrib_src_dir
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.framework_dir = os.path.normpath(os.path.join(this_dir, ".."))


    def get_config(self):
        """
        Returns:
            dict: Model configuration.
        """
        config_file_path = self.contrib_src_dir + "/model/config.json"
        return self._load_json(config_file_path)


    def get_legal(self):
        """
        Returns:
            dict:
                All of modelhub's, the model's, and the sample data's
                legal documents as dictionary. If one (or more) of the legal
                files don't exist, the error  will be logged with the
                corresponding key. Dictionary keys are:

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
        Returns:
            dict:
                The model's input/output sizes and types as dictionary.
                Convenience function, as this is a subset of what
                :func:`~get_config` returns
        """
        config_file_path = self.contrib_src_dir + "/model/config.json"
        config = self._load_json(config_file_path)
        if "error" in config:
            return config
        else:
            return config["model"]["io"]


    def get_samples(self):
        """
        Returns:
            dict:
                Folder and file names of sample data bundled with this model.
                The diconary key "folder" holds the absolute path to the
                sample data folder in the model container. The key "files"
                contains a list of all file names in that folder. Join these
                together to get the full path to the sample files.
        """
        try:
            sample_data_dir = self.contrib_src_dir + "/sample_data"
            _, _, sample_files = next(os.walk(sample_data_dir))
            return  {"folder": sample_data_dir,
                     "files": sample_files}
        except Exception as e:
            return {'error': repr(e)}


    def predict(self, input_file_path, numpyToFile=True, url_root=""):
        """
        Preforms the model's inference on the given input.

        Args:
            input_file_path (str): Path to input file to run inference on.
            numpyToFile (bool): Only effective if prediction is a numpy array.
                Indicates if numpy outputs should be saved and a path to it is
                returned. If false, a json-serializable list representation of
                the numpy array is returned instead. List representations is
                very slow with large numpy arrays.
            url_root (str): Url root added by the rest api.

        Returns:
            dict, list, or numpy array:
                Prediction result on input data. Return type/foramt as
                specified in the model configuration (see :func:`~get_model_io`).
                In case of an error, returns a dictionary
                with error info.
        """
        try:
            start = time.time()
            output = self.model.infer(input_file_path)
            output = self._correct_output_list_wrapping(output)
            end = time.time()
            config = self.get_config()
            output_list = []
            for i, o in enumerate(output):
                shape = list(o.shape) if isinstance(o, numpy.ndarray) else [len(o)]
                if isinstance(o, numpy.ndarray):
                    o = url_root + "api" + self._save_output(o) if numpyToFile else o.tolist()
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

    def _save_output(self, output):
        now = datetime.now()
        path = os.path.join(self.output_folder,
                                 "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"),
                                 "npy"))
        numpy.save(path, output, allow_pickle=False)
        return path
