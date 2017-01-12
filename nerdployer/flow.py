
import os
import re
import importlib
import inspect
import json
import logging
import yaml
from collections import defaultdict
from nerdployer.exceptions import StepExecutionException, FlowException
from nerdployer.step import BaseStep
from nerdployer.helpers.utils import render_template, parse_content

CONFIGURATION_ENTRY = 'configuration'
FLOW_ENTRY = 'flow'
STEPS_DEFINITIONS_ENTRY = 'steps'
RECOVERY_STEPS_DEFINITIONS_ENTRY = 'recovery'
ERROR_CONTEXT_ENTRY = 'error'

logger = logging.getLogger(__name__)


class NerdFlow():
    def __init__(self, nerdfile, context):
        self._nerdfile = nerdfile
        self._context = context

    def run(self):
        configuration, main_step_names, error_step_names = self._get_configuration_and_steps()
        all_steps_executors = self._load_steps_executors(configuration)
        logger.info('running flow... found: %s steps', len(main_step_names))
        try:
            self._run_steps_flow(all_steps_executors, main_step_names, STEPS_DEFINITIONS_ENTRY)
        except StepExecutionException as e:
            self._populate_context(ERROR_CONTEXT_ENTRY, {'step': e.step, 'exception': e.message})
            self._run_steps_flow(all_steps_executors, error_step_names, RECOVERY_STEPS_DEFINITIONS_ENTRY)
            raise e
        logger.info('done running flow...')

    def _run_steps_flow(self, all_steps_executors, step_names, entry_type):
        for step_name in step_names:
            step_definition = self._get_step_definition(step_name, entry_type)
            try:
                result = self._run_step_executor(
                    all_steps_executors, step_definition)
                if result:
                    self._populate_context(step_name, result)
            except Exception as e:
                logger.error('step %s failed... message : %s', step_name, str(e))
                if not step_definition.get('ignore_errors', False):
                    raise StepExecutionException(step_name, str(e))

    def _populate_context(self, step_name, result):
        self._context[step_name] = result

    def _run_step_executor(self, all_steps_executors, step_definition):
        step_executor = self._get_step_executor(all_steps_executors, step_definition['type'])
        logger.info('running step: %s', step_definition['name'])
        result = step_executor.execute(self._context, defaultdict(lambda: None, step_definition.get('parameters', {})))
        logger.info('done running step: %s', step_definition['name'])
        return result

    def _load_steps_executors(self, config):
        pysearchre = re.compile('.py$', re.IGNORECASE)
        steps_files = filter(pysearchre.search, os.listdir(os.path.join(os.path.dirname(__file__), 'steps')))
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

    def _get_step_definition(self, step_name, entry_type=STEPS_DEFINITIONS_ENTRY):
        nerdfile = self._load_nerdfile()
        return [step for step in nerdfile[FLOW_ENTRY][entry_type] if step['name'] == step_name][0]

    def _get_configuration_and_steps(self):
        nerdfile = self._load_nerdfile()
        configuration = nerdfile[CONFIGURATION_ENTRY]
        main_step_names = [step['name']for step in nerdfile[FLOW_ENTRY][STEPS_DEFINITIONS_ENTRY]]
        error_step_names = [step['name'] for step in nerdfile[FLOW_ENTRY][RECOVERY_STEPS_DEFINITIONS_ENTRY]]
        return configuration, main_step_names, error_step_names

    def _load_nerdfile(self):
        content = render_template(self._nerdfile, self._context)
        try:
            return parse_content(content)
        except:
            raise FlowException('invalid nerdfile... please provide a valid yaml or json file')
