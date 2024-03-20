# -*- coding: utf-8 -*-
"""
Test client
"""
import pathlib
import subprocess
import sys

CLI = pathlib.Path(__file__).parent.parent / "run-lottery.py"


def test_help():
    """test help"""
    subprocess.run([sys.executable, CLI, "--help"], check=True)
