import os
import logging
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('pyreleaser_io', 'res/templates')
)

logger = logging.getLogger(__name__)


def render(template_filename, **kwargs):
    template = env.get_template(template_filename)
    return template.render(kwargs)


def render_to_file(template_filename, target_filename=None, target_dir=None, **kwargs):
    _target_filename = target_filename or \
                      os.path.join(target_dir, template_filename.replace(".jinja2", ""))
    logger.debug(f"writing to {target_filename}")
    with open(_target_filename, 'w') as f:
        logger.debug(f"writing project file: {_target_filename} (args: {kwargs})")
        f.write(render(template_filename, **kwargs))
