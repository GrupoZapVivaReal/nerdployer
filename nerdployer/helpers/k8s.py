import subprocess


class K8s(object):

    def __init__(self, server, token, namespace, opts):
        self.server = server
        self.token = token
        self.namespace = namespace
        self.opts = opts

    def apply(self, template):
        apply_command = 'cat <<EOF | kubectl --server={server} --token={token} {namespace} {opts} ' \
                        'apply -f -\n{template}\nEOF'.format(
            server=self.server, token=self.token, template=template, opts=self.opts, namespace=self.namespace)
        return self._run_sub_process(apply_command)

    def rollout_status(self, deployment):
        check_command = 'kubectl --server={server} --token={token} {namespace} ' \
                        'rollout status deployment {deployment}'.format(
            server=self.server, token=self.token, deployment=deployment, namespace=self.namespace)
        return self._run_sub_process(check_command)

    def _run_sub_process(self, command):
        try:
            return subprocess.check_output([command], shell=True, stderr=subprocess.STDOUT).decode(
                'utf-8').strip()
        except subprocess.CalledProcessError as e:
            raise Exception(e.output.decode('utf-8').strip().replace('\n', ' - '))
