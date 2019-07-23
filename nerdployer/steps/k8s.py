from nerdployer.helpers.k8s import K8s
from nerdployer.step import BaseStep


class K8sStep(BaseStep):
    def __init__(self, config):
        super().__init__('k8s', config)

    def execute(self, context, params):
        k8s = K8s(self.config)
        operation = params.get('operation', 'apply')

        if 'apply' in operation:
            result = k8s.apply(context, params)
        if 'rollout_status' in operation:
            result = k8s.rollout_status(context, params)

        return result
