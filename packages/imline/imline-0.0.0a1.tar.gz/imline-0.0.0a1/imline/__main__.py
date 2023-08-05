#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __main__
    :platform: Unix
    :synopsis: the top-level module of ImLine that contains the entry point and handles built-in commands.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import argparse
import os
import sys

from imline.logging import LogManager

import imline.__init__
from imline import dot_imline_dir

logger = None


def start(args):
    """Function that starts the ImLine with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """

    try:
        pass

    except KeyboardInterrupt:
        logger.debug("Keyboard Interruption")


def start_sub(args):
    """Function that starts the ImLine with the sub jobs according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """

    if args["sub_jobs"] == "set-key-points":
        imline.mapper.start_by(raw_dataset=args["raw_dataset"])


def prepare(args):
    """The function that prepares the working environment for storing data during running.

    Args:
        args:       Command-line arguments.
    """
    from imline.presentation import startup_banner
    startup_banner()

    if not os.path.exists(dot_imline_dir):
        os.mkdir(dot_imline_dir)

    imline.log_manager = LogManager(args)

    global logger
    logger = imline.log_manager.get_logger(__name__, "DEBUG")
    logger.info("Logger integration successful.")

    from imline.mapping import Mapper

    imline.mapper = Mapper(args["output"])

    if args["sub_jobs"]:
        start_sub(args)
        sys.exit(1)


def initiate():
    """The top-level method to serve as the entry point of ImLine.

    This method is the entry point defined in `setup.py` for the `imline` executable that placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()

    other_gr = ap.add_argument_group('Others')
    other_gr.add_argument('--ripe-dataset', help='Images folder that keeps already marked images and their key-points\'s JSON data.', type=str)
    other_gr.add_argument("--environment", help="The running environment. It specify the configuration files and logs. To use: either `production`, `development` or `testing`. Default is production", action="store", type=str, choices=["production", "development", "testing"], default="development")
    other_gr.add_argument("-v", "--verbose", help="Print various debugging logs to console for debug problems", action="store_true")
    other_gr.add_argument("--version", help="Display the version number of ImLine.", action="store_true")

    sub_p = ap.add_subparsers(dest="sub_jobs", help='officiate the sub-jobs')  # if sub-commands not used their arguments create raise.

    ap_key_po = sub_p.add_parser('set-key-points', help='Mark key-points of the given images to the ImLine.')
    ap_key_po.add_argument('--raw-dataset', help='Images folder that will be marked for specifying key-points.', type=str)
    ap_key_po.add_argument('--output', help='Data folder path that will be keep key-point coordinates and mapped image files.', type=str)

    args = vars(ap.parse_args())

    if args["version"]:
        from imline.presentation import versions_banner
        versions_banner()
        sys.exit(1)

    prepare(args)
    start(args)


if __name__ == '__main__':
    initiate()
