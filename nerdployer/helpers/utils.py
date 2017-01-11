
import pystache


def fallback(list):
    return next((item for item in list if item), None)


def render_template(file, params):
    with open(file) as f:
        return pystache.render(f.read(), params)
