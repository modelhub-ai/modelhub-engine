from modelhubapi.pythonapi import ModelHubAPI

class MonkeyPythonAPI(ModelHubAPI):
    """
    This class enables monkeypatching of the REST API by
    overriding the methods that set the configuration file.
    This allows us to use configuration files independently from model
    directories during testing which is not needed in production.
    """

    def __init__(self, model, contrib_src_dir, config):
        self.monekyconfig = contrib_src_dir + "/model/" + config
        super(MonkeyPythonAPI, self).__init__(model, contrib_src_dir)

    def get_config(self):
        return self._load_json(self.monkeyconfig)
