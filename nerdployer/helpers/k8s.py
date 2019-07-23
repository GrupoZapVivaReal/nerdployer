import subprocess


class K8s(object):

    def __init__(self, config):
        self.config = config

    def apply(self, server, token, template, opts, namespace):
        apply_command = 'cat <<EOF | kubectl --server={server} --token={token} {namespace} {opts} ' \
                        'apply -f -\n{template}\nEOF'.format(
            server=server, token=token, template=template, opts=opts, namespace=namespace)
        return self._run_sub_process(apply_command)

    def rollout_status(self, server, token, deployment, namespace):
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
