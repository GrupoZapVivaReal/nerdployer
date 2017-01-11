
from nerdployer.step import BaseStep
from nerdployer.helpers.docker import Docker


class DockerStep(BaseStep):
    def __init__(self, config):
        super().__init__('docker', config)

    def execute(self, context, params):
        client = Docker()
        operation = params['operation']
        if operation == 'build_and_push':
            result = client.build_and_push(params['respository'], params['tag'], params['path'])
        else:
            raise ValueError('invalid operation')

        return result
