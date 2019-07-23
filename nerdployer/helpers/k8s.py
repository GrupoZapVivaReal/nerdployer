import subprocess

import nerdployer.helpers.utils as utils


class K8s(object):

    def __init__(self, config):
        self.config = config

    def apply(self, context, params):
        server = self.config['server']
        token = self.config['token']
        opts = self.config['opts'] or ''
        namespace = self.config['namespace'] or ''
        context_mappings = {**context, **params.get('mappings', {})}
        parameters_mappings = utils.parse_content(utils.render_template(params['parameters'], context_mappings)) if \
            params['parameters'] else {}
        full_mappings = {**context_mappings, **parameters_mappings}
        template = utils.render_template(params['template'], full_mappings)
        apply_command = 'cat <<EOF | kubectl --server={server} --token={token} {namespace} {opts} ' \
                        'apply -f -\n{template}\nEOF'.format(
            server=server, token=token, template=template, opts=opts, namespace=namespace)
        return self._run_sub_process(apply_command)

    def rollout_status(self, context, params):
        server = self.config['server']
        token = self.config['token']
        namespace = self.config['namespace'] or ''
        deployment = params['deployment']

        check_command = 'kubectl --server={server} --token={token} {namespace} ' \
                        'rollout status deployment {deployment}'.format(
            server=server, token=token, deployment=deployment, namespace=namespace)
        return self._run_sub_process(check_command)

    def _run_sub_process(self, command):
        try:
            return subprocess.check_output([command], shell=True, stderr=subprocess.STDOUT).decode(
                'utf-8').strip()
        except subprocess.CalledProcessError as e:
            raise Exception(e.output.decode('utf-8').strip().replace('\n', ' - '))
