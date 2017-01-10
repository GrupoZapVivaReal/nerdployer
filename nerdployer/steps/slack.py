
from nerdployer.step import BaseStep
from nerdployer.helpers.slack import Slack


class SlackStep(BaseStep):
    def __init__(self, config):
        super().__init__('slack', config)

    def process(self, step_name, context, params):
        Slack.notify(params['webhook'], params['channel'], params['icon'], params['bot'], params['message'])
