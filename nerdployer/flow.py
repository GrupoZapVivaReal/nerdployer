
import os
import re
import importlib
import inspect
import json
import logging
from collections import defaultdict
from nerdployer.step import BaseStep
from nerdployer.helpers.utils import render_template

CONFIGURATION_ENTRY = 'configuration'
STEPS_ENTRY = 'steps'

logger = logging.getLogger(__name__)


class Flow():
    def __init__(self, nerdfile, context):
        self._nerdfile = nerdfile
        self._context = context

    def run(self):
        configuration, step_names = self._get_configuration_and_steps()
        all_steps_executors = self._load_steps_executors(configuration)
        logger.info('running flow... found: %s steps', len(step_names))
        for step_name in step_names:
            step = self._get_step_definition(step_name)
            step_executor = self._get_step_executor(all_steps_executors, step['type'])
            logger.info('running step: %s', step_name)
            step_executor.run(step_name, self._context, defaultdict(lambda: None, step.get('parameters', {})))
            logger.info('done running step: %s', step_name)
        logger.info('done running flow...')

    def _load_steps_executors(self, config):
        pysearchre = re.compile('.py$', re.IGNORECASE)
        steps_files = filter(pysearchre.search, os.listdir(
            os.path.join(os.path.dirname(__file__), 'steps')))
        steps = map(lambda name: '.' + os.path.splitext(name)[0], steps_files)
        importlib.import_module('nerdployer.steps')
        loaded_steps = []
        for step in steps:
            if not '__init__' in step:
                step_module = importlib.import_module(step, package='nerdployer.steps')
                for entry in dir(step_module):
                    entry_module = getattr(step_module, entry)
                    if inspect.isclass(entry_module) and issubclass(entry_module, BaseStep) and entry_module.__name__ != BaseStep.__name__:
                        loaded_steps.append(entry_module(config))

        return loaded_steps

    def _get_step_executor(self, step_executors, type):
        return [step for step in step_executors if step.type == type][0]

    def _get_step_definition(self, step_name):
        configuration = self._load_nerdfile()
        return [step for step in configuration[STEPS_ENTRY] if step['name'] == step_name][0]

    def _get_configuration_and_steps(self) :
        nerdfile = self._load_nerdfile()
        configuration = nerdfile[CONFIGURATION_ENTRY]
        step_names = [step['name'] for step in nerdfile[STEPS_ENTRY]]
        return configuration, step_names

    def _load_nerdfile(self):
        content = render_template(self._nerdfile, self._context)
        return json.loads(content)
