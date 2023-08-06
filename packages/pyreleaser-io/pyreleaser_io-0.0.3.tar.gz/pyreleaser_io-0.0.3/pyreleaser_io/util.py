import logging
import sys
import pathlib
import os
import yaml
import subprocess

logger = logging.getLogger(__name__)


def setup_logging(level, logger_name=__name__):
    _logger = logging.getLogger(logger_name)
    _logger.setLevel(level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s"))
    _logger.addHandler(console_handler)

    _logger.debug("====[debug mode enabled]====")


def settings():
    settings_file = os.path.join(str(pathlib.Path.home()), ".pyreleaser_io.yaml")
    if os.path.isfile(settings_file):
        logger.debug("parsing: %s", settings_file)
        with open(settings_file, 'r') as f:
            data = yaml.safe_load(f.read())
    else:
        logging.warning(f"skipping missing settings file: {settings_file}")
        data = {}

    return data.get("pyreleaser_io", {})


def run(cmd, check=True):
    """
    run a command, return output
    cmd - command to run (array)

    """
    try:
        # RHEL8 uses python 3.6 so we're stuck with `check_output()` for the next
        # few years
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        if check:
            raise e

        output = e.output
    return output.decode().strip()
