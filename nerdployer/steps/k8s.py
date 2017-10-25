
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

        if params['content']:
            template = utils.render_content(params['content'], params.get('mappings', context))
        else:
            template = utils.render_template(params['file'], params.get('mappings', context))

        apply_command = 'cat <<EOF | kubectl --server={server} --token={token} {opts} apply -f -\n{template}\nEOF'.format(server=server, token=token, template=template, opts=opts)

        return subprocess.check_output([apply_command], shell=True).decode('utf-8').strip()
