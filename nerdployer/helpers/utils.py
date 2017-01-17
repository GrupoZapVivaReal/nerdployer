
from jinja2 import Environment, Undefined
import json
import yaml
from collections import defaultdict


class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''


def fallback(list):
    return next((item for item in list if item), None)


def render_template(file, params):
    with open(file) as f:
        return render_content(f.read(), params)


def render_content(content, params, start_delimiter='{{', end_delimiter='}}'):
    template = Environment(undefined=SilentUndefined, variable_start_string=start_delimiter, variable_end_string=end_delimiter).from_string(content)
    return template.render(params)


def parse_content(content):
    try:
        return json.loads(content)
    except:
        try:
            return yaml.safe_load(content)
        except:
            raise ValueError('could not parse the content as an valid yaml or json')


def safe_dict(current_dict):
    return defaultdict(lambda: None, current_dict)
