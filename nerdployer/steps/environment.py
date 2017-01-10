
from nerdployer.step import BaseStep
import os


class EnvironmentStep(BaseStep):
    def __init__(self, config):
        super().__init__('environment', config)

    def process(self, step_name, context, params):
        context[step_name] = {}
        for key, value in params.items():
            env_value = os.getenv(key)
            if env_value:
                context[step_name][value] = env_value
