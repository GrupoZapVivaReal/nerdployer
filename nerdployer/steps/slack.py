
from nerdployer.step import BaseStep
from nerdployer.helpers.slack import Slack
import nerdployer.helpers.utils as utils


class SlackStep(BaseStep):
    def __init__(self, config):
        super().__init__('slack', config)

    def execute(self, step_name, context, params):
        webhook = utils.fallback([params['webhook'], self.config['webhook']])
        channel = utils.fallback([params['channel'], self.config['channel']])
        icon = utils.fallback([params['icon'], self.config['icon']])
        bot = utils.fallback([params['bot'], self.config['bot']])
        message = utils.fallback([params['message'], self.config['message']])
        Slack.notify(webhook, channel, icon, bot, message)
