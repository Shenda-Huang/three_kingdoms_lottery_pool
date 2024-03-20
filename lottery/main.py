# -*- coding: utf-8 -*-
""" Table settings module """
import argparse
import logging
import sys
import traceback
from typing import List, Optional

from .args import parse_cmdline
from .exceptions import LocalRuntimeError
from .process_lottery import run_scenarios

LOGGER = logging.getLogger(__name__)


def run(
    taskname: Optional[str],
    log_file: Optional[str],
    log_level: str,
    num_users: List[int],
) -> int:
    """run"""

    if log_file is None:
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s:%(lineno)s ",
            handlers=[logging.StreamHandler()],
        )
    else:
        logging.basicConfig(
            filename=log_file,
            filemode='w',
            level=log_level,
            format="%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s:%(lineno)s ",
        )

    LOGGER.info("Starting task %s", taskname)

    run_scenarios(num_users)

    LOGGER.info("Task %s finished", taskname)

    return 0


def main() -> int:
    """main"""
    rcode = 255

    try:
        args: argparse.Namespace = parse_cmdline()
        rcode = run(**vars(args))
    except argparse.ArgumentError as exc:
        print("".join(traceback.format_exception_only(type(exc), exc)), file=sys.stderr)
    except SystemExit as exc:
        rcode = 0 if exc.code is None else int(exc.code)
    except LocalRuntimeError as exc:
        LOGGER.error("Runtime error for run lottery", exc_info=True)

    return rcode


if __name__ == "__main__":
    sys.exit(main())
