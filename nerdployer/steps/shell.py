
from nerdployer.step import BaseStep
import subprocess


class ShellStep(BaseStep):
    def __init__(self, config):
        super().__init__('shell', config)

    def execute(self, step_name, context, params):
        ouput = subprocess.check_output(params['commands']).decode("utf-8").strip()
        return ouput
