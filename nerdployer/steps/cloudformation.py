
from nerdployer.step import BaseStep
from nerdployer.helpers.cloudformation import Cloudformation
import nerdployer.helpers.utils as utils


class CloudformationStep(BaseStep):
    def __init__(self, config):
        super().__init__('cloudformation', config)

    def execute(self, context, params):
        region = utils.fallback([params['region'], self.config['region'], 'us-east-1'])
        client = Cloudformation(region)
        operation = params['operation']
        if operation == 'create_or_update':
            template = utils.render_template(params['template'], context)
            parameters = utils.render_template(params['parameters'], context)
            stack = client.get_stack(params['stack'])
            if not stack:
                result = client.create_stack(params['stack'], template, parameters, params['tags'])
            else:
                result = client.update_stack(params['stack'], template, parameters, params['tags'])
        elif operation == 'delete_stack':
            result = client.delete_stack(params['stack'])
        elif operation == 'list_stacks':
            result = client.list_stacks(params['tags'])
        elif operation == 'get_stack_resources':
            result = client.get_stack_resources(params['stack'])
        elif operation == 'get_stack_resource':
            result = client.get_stack_resource(params['stack'], params['resource'])
        else:
            raise ValueError('invalid operation')

        return result
