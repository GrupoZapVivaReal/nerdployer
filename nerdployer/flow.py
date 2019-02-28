
import os
import re
import importlib
import inspect
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from nerdployer.exceptions import StepExecutionException, FlowException
from nerdployer.step import BaseStep
from nerdployer.helpers.utils import render_template, parse_content, safe_dict

CONFIGURATION_ENTRY = 'configuration'
FLOW_ENTRY = 'flow'
FAILURE_ENTRY = 'failure'
ERROR_CONTEXT_ENTRY = 'error'
MAX_WORKERS = int(os.getenv('MAX_WORKERS', 10))

logger = logging.getLogger(__name__)


class NerdFlow():
    def __init__(self, nerdfile, context):
        self._nerdfile = nerdfile
        self._context = context
        self._async_tasks = {}
        self._async_executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    def run(self):
        configuration, main_steps, error_steps = self._get_configuration_and_steps()
        all_steps_executors = self._load_steps_executors(configuration)
        logger.info('running flow... found: %s steps', len(main_steps))
        try:
            self._run_steps_flow(all_steps_executors, main_steps, FLOW_ENTRY)
        except StepExecutionException as e:
            self._populate_context(ERROR_CONTEXT_ENTRY, {'step': e.step, 'exception': e.message})
            self._run_steps_flow(all_steps_executors, error_steps, FAILURE_ENTRY)
            raise e
        self._async_executor.shutdown()
        logger.info('done running flow...')

    def _run_steps_flow(self, all_steps_executors, steps, entry_type):
        def _run_step(step):
            self._wait_for(step['depends_on'])
            step_definition = self._get_step_definition(step['name'], entry_type)
            try:
                result = self._run_step_executor(
                    all_steps_executors, step_definition)
                if result:
                    self._populate_context(step['name'], result)
            except Exception as e:
                logger.error('step %s failed... message : %s', step['name'], str(e))
                if not step_definition.get('ignore_errors', False):
                    raise StepExecutionException(step['name'], str(e))

        for step in steps:
            future = self._async_executor.submit(_run_step, step)
            self._async_tasks[step['name']] = future
            if not step['async']:
                future.result()

    def _populate_context(self, step_name, result):
        self._context[step_name] = result

    def _run_step_executor(self, all_steps_executors, step_definition):
        step_executor = self._get_step_executor(all_steps_executors, step_definition['type'])
        logger.info('running step: %s', step_definition['name'])
        result = step_executor.execute(self._context, safe_dict(step_definition.get('parameters', {})))
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

    def _get_step_definition(self, step_name, entry_type):
        nerdfile = self._load_nerdfile()
        return [step for step in nerdfile[entry_type] if step['name'] == step_name][0]

    def _get_configuration_and_steps(self):
        nerdfile = self._load_nerdfile()
        configuration = nerdfile.get(CONFIGURATION_ENTRY, {})
        flow_steps = [{'name': step['name'], 'async': step.get('async', False), 'depends_on': step.get('depends_on', [])} for step in nerdfile.get(FLOW_ENTRY, [])]
        failure_steps = [{'name': step['name'], 'async': step.get('async', False), 'depends_on': step.get('depends_on', [])}  for step in nerdfile.get(FAILURE_ENTRY, [])]
        return configuration, flow_steps, failure_steps

    def _wait_for(self, steps):
        for future in as_completed([self._async_tasks[step] for step in steps]):
            future.result()

    def _load_nerdfile(self):
        content = render_template(self._nerdfile, self._context)
        try:
            return parse_content(content)
        except:
            raise FlowException('invalid nerdfile... please provide a valid yaml or json file')
