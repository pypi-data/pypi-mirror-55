import argparse
import logging
import pyreleaser_io.util
import pkg_resources
import pyreleaser_io.create
import pyreleaser_io.util

logger = logging.getLogger(__name__)


def version():
    return pkg_resources.require("pyreleaser_io")[0].version


def main():
    parser = argparse.ArgumentParser(description="""
    pyreleaser - python release helper tool
    """)

    parser.add_argument('--debug',
                        default=False,
                        action='store_true',
                        help='debug mode enabled')
    parser.add_argument('--version',
                        default=False,
                        action='store_true',
                        help='Print the sysdef version and exit')
    parser.add_argument('--create-project',
                        default=False,
                        action='store_true',
                        help='create a project')
    args = parser.parse_args()
    pyreleaser_io.util.setup_logging(
        logging.DEBUG if args.debug else logging.INFO, "pyreleaser_io"
    )

    settings = pyreleaser_io.util.settings()

    if args.version:
        print(version())
    elif args.create_project:
        pyreleaser_io.create.interactive(settings)
    else:
        parser.print_usage()
