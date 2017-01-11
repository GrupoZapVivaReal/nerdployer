
from nerdployer.step import BaseStep
import os


class EnvironmentStep(BaseStep):
    def __init__(self, config):
        super().__init__('environment', config)

    def execute(self, context, params):
        result = {}
        for key, value in params.items():
            env_value = os.getenv(key)
            if env_value:
                result[value] = env_value

        return result
