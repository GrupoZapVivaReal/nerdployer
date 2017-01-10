import logging
import json
from docker import Client


class Docker(object):

    def __init__(self):
        self._client = Client(version='auto')

    def build_and_push(self, repository, tag, path):
        self._log_stream('building', self._client.build(tag=repository + ':' + tag, path=path, stream=True))
        self._log_stream('pushing', self._client.push(repository=repository, tag=tag, stream=True))

    def _log_stream(self, phase, stream):
        for output in stream:
            try:
                output = json.loads(output.decode('utf-8'))
            except:
                pass

            logging.info('%s --> %s', phase, output)
