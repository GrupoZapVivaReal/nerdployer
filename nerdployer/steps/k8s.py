
import subprocess
from nerdployer.step import BaseStep
import nerdployer.helpers.utils as utils


class K8sStep(BaseStep):
    def __init__(self, config):
        super().__init__('k8s', config)

    def execute(self, context, params):
        server = self.config['server']
        token = self.config['token']
        opts = self.config['opts'] or ''
        context_mappings = {**context, **params.get('mappings', {})}
        parameters_mappings = utils.parse_content(utils.render_template(params['parameters'], context_mappings)) if params['parameters'] else {}
        full_mappings = {**context_mappings, **parameters_mappings}
        template = utils.render_template(params['template'], full_mappings)
        apply_command = 'cat <<EOF | kubectl --server={server} --token={token} {opts} apply -f -\n{template}\nEOF'.format(server=server, token=token, template=template, opts=opts)
        try:
            return subprocess.check_output([apply_command], shell=True, stderr=subprocess.STDOUT).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            raise Exception(e.output.decode('utf-8').strip().replace('\n', ' - '))
