from collections import defaultdict

class BaseStep(object):
    def __init__(self, type, config):
        self.type = type
        self.config = defaultdict(lambda: None)
        if type in config:
            self.config = defaultdict(lambda: None, config[self._type])

    def execute(self, step_name, context, params):
        raise NotImplementedError('please implement this method')

    def run(self, step_name, context, params):
        result = self.execute(step_name, context, params)
        if result:
            context[step_name] = result

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
