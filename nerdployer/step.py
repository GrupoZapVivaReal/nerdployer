

class BaseStep(object):
    def __init__(self, step_type, config):
        self.step_type = step_type
        self.config = config[step_type]

    def execute(self, step_name, context, params=None):
        pass
