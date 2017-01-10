
from nerdployer.step import BaseStep
import subprocess


class GitStep(BaseStep):
    def __init__(self, config):
        super().__init__('git', config)

    def process(self, step_name, context, params):
        version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8").strip()
        context[step_name] = version
