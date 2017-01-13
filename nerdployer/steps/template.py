
from nerdployer.step import BaseStep
import nerdployer.helpers.utils as utils

DEFAULT_CONTENT_DELIMITER = ('[[', ']]')


class TemplateStep(BaseStep):
    def __init__(self, config):
        super().__init__('template', config)

    def execute(self, context, params):
        content = params['content']
        file = params['file']

        mappings = params.get('mappings', context)

        if content:
            return utils.render_content(content, mappings, DEFAULT_CONTENT_DELIMITER)
        else:
            return utils.render_template(file, mappings)
