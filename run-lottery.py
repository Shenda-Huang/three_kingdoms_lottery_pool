"""run lottery as module
"""

# pylint: disable=invalid-name
import runpy

runpy.run_module("lottery", run_name="__main__", alter_sys=True)
