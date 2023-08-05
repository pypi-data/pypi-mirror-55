# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = django_oscar_dsd.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging

from django_oscar_dsd import __version__

from django_oscar_dsd import settings, functions

__author__ = "pai"
__copyright__ = "pai"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(parser, args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version="django-oscar-dsd {ver}".format(ver=__version__))

    parser.add_argument(
        dest="action",
        help="One of {}".format(settings.ACTIONS))

    parser.add_argument(
        "-p",
        "--page",
        dest="page",
        help="set dsd pagination page")

    parser.add_argument(
        "-l",
        "--limit",
        dest="limit",
        help="set max number of items to load")

    parser.add_argument(
        "-po",
        "--parse-only",
        dest="parse_only",
        help="do not publish items",
        action="store_const",
        const=True)

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    parser = argparse.ArgumentParser(
        description="Django Oscar Vue DSD integration")

    args = parse_args(parser, args)
    setup_logging(args.loglevel)

    action = args.action
    if action not in settings.ACTIONS:
        raise parser.error('Action {} not available.'.format(action))
    else:
        _logger.info('Running: {}'.format(action))

        parse_only = args.parse_only

        if action == 'list_dsd_products':
            page = args.page
            # if page is None:
            #     parser.error('Missing page.')

            ret = functions.list_dsd_products(page=page, logger=_logger)

            print(ret)

        elif action == 'load_dsd_backend_products':
            limit = args.limit

            ret = functions.load_dsd_backend_products(limit=limit, publish=not parse_only,
                                                      logger=_logger)

            print(ret)

        _logger.info("Script ended")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
