
from nerdployer.step import BaseStep
import pprint


class EchoStep(BaseStep):
    def __init__(self, config):
        super().__init__('echo', config)

    def execute(self, context, params):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(context)
        pp.pprint(params)