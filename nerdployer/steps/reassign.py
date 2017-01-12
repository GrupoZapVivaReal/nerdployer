
from nerdployer.step import BaseStep


class ReAssignStep(BaseStep):
    def __init__(self, config):
        super().__init__('reassign', config)

    def execute(self, context, params):
        return params
