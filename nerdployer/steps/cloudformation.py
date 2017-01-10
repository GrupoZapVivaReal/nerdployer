
from nerdployer.step import BaseStep
from nerdployer.helpers.cloudformation import Cloudformation


class CloudformationStep(BaseStep):
    def __init__(self, config):
        super().__init__('cloudformation', config)

    def process(self, step_name, context, params):
        client = Cloudformation(self.config['region'])
        operation = params['operation']
        if operation == 'create_or_update':
            stack = client.get_stack(params['stack'])
            if not stack:
                result = client.create_stack(params['stack'], params['template'], params['parameters'], params['tags'])
            else:
                result = client.update_stack(params['stack'], params['template'], params['parameters'], params['tags'])
        elif operation == 'delete_stack':
            result = client.delete_stack(params['stack'])
        elif operation == 'list_stacks':
            result = client.list_stacks(params['tags'])
        elif operation == 'get_stack_resources':
            result = client.get_stack_resources(params['stack'])
        elif operation == 'get_stack_resource':
            result = client.get_stack_resource(
                params['stack'], params['resource'])
        else:
            raise ValueError('invalid operation')

        context[step_name] = result
