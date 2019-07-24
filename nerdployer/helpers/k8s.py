import subprocess


class K8s(object):

    def __init__(self, server, token, namespace, opts):
        self.base_cmd = 'kubectl --server={server} --token={token}' \
                        ' -n {namespace} {opts} '.format(server=server,
                                                         token=token,
                                                         namespace=namespace,
                                                         opts=opts)

    def apply(self, template):
        apply_command = 'cat <<EOF | {base_cmd} --record --validate=false ' \
                        'apply -f -\n{template}\nEOF'.format(
            template=template, base_cmd=self.base_cmd)
        return self._run_sub_process(apply_command)

    def rollout_status(self, deployment):
        check_command = '{base_cmd} ' \
                        'rollout status deployment {deployment}'.format(
            deployment=deployment, base_cmd=self.base_cmd)
        return self._run_sub_process(check_command)

    def _run_sub_process(self, command):
        try:
            return subprocess.check_output([command], shell=True, stderr=subprocess.STDOUT).decode(
                'utf-8').strip()
        except subprocess.CalledProcessError as e:
            raise Exception(e.output.decode('utf-8').strip().replace('\n', ' - '))
