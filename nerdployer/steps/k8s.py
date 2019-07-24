import nerdployer.helpers.utils as utils
from nerdployer.helpers.k8s import K8s
from nerdployer.step import BaseStep


class K8sStep(BaseStep):
    def __init__(self, config):
        super().__init__('k8s', config)

    def execute(self, context, params):
        k8s = K8s(self.config['server'], self.config['token'], self.config['namespace'],
                  self.config['opts'] or '')
        operation = params.get('operation', 'apply')

        if 'apply' in operation:
            result = k8s.apply(self._prepare_template(context, params))
        if 'rollout_status' in operation:
            result = k8s.rollout_status(params['deployment'])

        return result

    def _prepare_template(self, context, params):
        context_mappings = {**context, **params.get('mappings', {})}
        parameters_mappings = utils.parse_content(
            utils.render_template(params['parameters'], context_mappings)) \
            if params['parameters'] else {}
        full_mappings = {**context_mappings, **parameters_mappings}
        return utils.render_template(params['template'], full_mappings)
