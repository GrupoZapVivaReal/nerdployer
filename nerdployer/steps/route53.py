
from nerdployer.step import BaseStep
from nerdployer.helpers.route53 import Route53


class Route53Step(BaseStep):
    def __init__(self, config):
        super().__init__('route53', config)

    def execute(self, step_name, context, params):
        client = Route53()
        operation = params['operation']
        if operation == 'create_or_update':
            result = client.create_record(self.config['hostedzoneid'], params['record'], params['target'], params['type'], params['ttl'])
        else:
            raise ValueError('invalid operation')

        return result
