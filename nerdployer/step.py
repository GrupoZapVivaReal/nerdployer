from collections import defaultdict

class BaseStep(object):
    def __init__(self, type, config):
        self.type = type
        self.config = defaultdict(lambda: None)
        if type in config:
            self.config = defaultdict(lambda: None, config[self._type])

    def execute(self, context, params):
        raise NotImplementedError('please implement this method')

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type
