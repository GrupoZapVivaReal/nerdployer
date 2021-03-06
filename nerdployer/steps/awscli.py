
from nerdployer.step import BaseStep
import nerdployer.helpers.utils as utils
import subprocess
import json


class AwsCliStep(BaseStep):
    def __init__(self, config):
        super().__init__('awscli', config)

    def execute(self, context, params):
        region = utils.fallback([params['region'], self.config['region'], 'us-east-1'])
        command = ['aws', params['service'], params['command']] + params.get('arguments', []) + ['--region', region, '--output', 'json']
        ouput = subprocess.check_output(command).decode("utf-8").strip() or '{}'
        return json.loads(ouput)
