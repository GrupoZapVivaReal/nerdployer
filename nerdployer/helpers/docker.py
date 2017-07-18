import logging
import docker

logger = logging.getLogger(__name__)


class Docker(object):

    def __init__(self):
        self._client = docker.from_env(version='auto')

    def build_and_push(self, repository, tag, path):
        logger.info('starting image building: {}:{} in {}'.format(repository, tag, path))
        self._client.images.build(tag='{}:{}'.format(repository, tag), path=path)
        logger.info('done image building: {}:{} in {}'.format(repository, tag, path))
        logger.info('starting image pushing: {}:{} in {}'.format(repository, tag, path))
        output = self._client.images.push(repository=repository, tag=tag)
        logger.info('done image pushing: {}:{} in {}'.format(repository, tag, path))
        logger.debug('image pushing output {}:{} - {}'.format(repository, tag, output))
