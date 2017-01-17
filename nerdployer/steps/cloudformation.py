
import os
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
        stack = params['stack']

        if operation == 'create_or_update':
            result = self._create_or_update_stack_action(client, stack, context, params)
        elif operation == 'delete_stack':
            result = client.delete_stack(stack)
        elif operation == 'list_stacks':
            result = client.list_stacks(params['tags'])
        elif operation == 'get_stack':
            result = client.get_stack(stack)
        elif operation == 'get_stack_resources':
            result = client.get_stack_resources(stack)
        elif operation == 'get_stack_resource':
            result = client.get_stack_resource(stack, params['resource'])
        else:
            raise ValueError('invalid operation')

        return result

    def _create_or_update_stack_action(self, client, stack, context, params):
        template_definition = params['template']
        if template_definition['provided']:
            template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates', template_definition['provided'])
        else:
            template_path = template_definition['external']

        template = utils.render_template(template_path, template_definition.get('mappings', context))
        parameters = utils.parse_content(utils.render_template(template_definition['parameters'], template_definition.get('mappings', context)))

        if not client.get_stack(stack):
            create_or_update = client.create_stack
        else:
            create_or_update = client.update_stack

        return create_or_update(stack, template, parameters, template_definition['tags'])
