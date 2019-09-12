from modelhubapi.pythonapi import ModelHubAPI

class Monkey(ModelHubAPI):

    def __init__(self, model, contrib_src_dir, config):
        self.monekyconfig = contrib_src_dir + "/model/" + config
        super(Monkey, self).__init__(model, contrib_src_dir)

    def get_config(self):
        return self._load_json(self.monkeyconfig)
