
from nerdployer.step import BaseStep
from nerdployer.helpers.cloudformation import Cloudformation
import nerdployer.helpers.utils as utils
import logging


logger = logging.getLogger(__name__)


class OldStackCleanerStep(BaseStep):
    def __init__(self, config):
        super().__init__('old_stack_cleaner', config)

    def execute(self, context, params):
        region = utils.fallback([params['region'], self.config['region']])
        client = Cloudformation(region)

        current_stack = params['current_stack']
        common_tags = params['common_tags']

        stacks = client.list_stacks(common_tags)
        for stack in stacks:
            if current_stack != stack['StackName']:
                logger.info('deleting stack: %s', stack['StackName'])
                client.delete(stack['StackName'])
