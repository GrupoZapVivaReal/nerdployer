
import pystache
import pystache.defaults
import json
import yaml

DEFAULT_PYSTACHE_DELIMITER = pystache.defaults.DELIMITERS


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
