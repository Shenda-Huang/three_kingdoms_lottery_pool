# -*- coding: utf-8 -*-
"""
arg parser
"""

import argparse

from .utils import Settings


def parse_cmdline() -> argparse.Namespace:
    """parse cmdline"""
    parser = argparse.ArgumentParser()

    parser.add_argument("taskname")
    parser.add_argument("-l", "--log-file")
    parser.add_argument("--log-level", default="INFO", choices=Settings.LOG_LEVELS)
    parser.add_argument(
        "-n",
        "--num-users",
        required=True,
        type=int,
        nargs="+",
        help="Number of users who entered in the lottery",
    )

    return parser.parse_args()
