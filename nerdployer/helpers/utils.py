
import pystache
import pystache.defaults
import json
import yaml
from collections import defaultdict

DEFAULT_PYSTACHE_DELIMITER = pystache.defaults.DELIMITERS
pystache.defaults.TAG_ESCAPE = lambda s: s.replace('\n', '\\n')


def fallback(list):
    return next((item for item in list if item), None)


def render_template(file, params, delimiters=DEFAULT_PYSTACHE_DELIMITER):
    with open(file) as f:
        return render_content(f.read(), params, delimiters)


def render_content(content, params, delimiters=DEFAULT_PYSTACHE_DELIMITER):
    pystache.defaults.DELIMITERS = delimiters
    rendered = pystache.render(content, params)
    pystache.defaults.DELIMITERS = DEFAULT_PYSTACHE_DELIMITER
    return rendered


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
