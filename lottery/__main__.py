# -*- coding: utf-8 -*-
"""
This module is needed when calling python -m lottery
"""

import sys

from . import main

if __name__ == "__main__":
    sys.exit(main.main())
