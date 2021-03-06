
from nerdployer.step import BaseStep
import nerdployer.helpers.utils as utils

START_DELIMITER = '[['
END_DELIMITER = ']]'


class TemplateStep(BaseStep):
    def __init__(self, config):
        super().__init__('template', config)

    def execute(self, context, params):
        content = params['content']
        file = params['file']
        mappings = {**context, **params.get('mappings', {})}

        if content:
            return utils.render_content(content, mappings, START_DELIMITER, END_DELIMITER)
        else:
            return utils.render_template(file, mappings)
