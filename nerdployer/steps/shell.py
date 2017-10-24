
from nerdployer.step import BaseStep
import subprocess


class ShellStep(BaseStep):
    def __init__(self, config):
        super().__init__('shell', config)

    def execute(self, context, params):
        ouput = subprocess.check_output(params['commands'], shell=params['shell_mode']).decode("utf-8").strip()
        return ouput
