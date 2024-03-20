# -*- coding: utf-8 -*-
"""
utils with all global variables and helper functions
"""

import datetime
import json
import logging

LOGGER = logging.getLogger(__name__)


class Settings:
    """settings"""

    # File path here are all relative path from the project root
    POOL_FILE_PATH = "input_files/Pool.xlsx"
    ITEMS_FILE_PATH = "input_files/Items.xlsx"
    CASH_FILE_PATH = "input_files/Cash.xlsx"
    DEBUG_MODE = False
    LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class DateTimeEncoder(json.JSONEncoder):
    """subclass JSONEncoder"""

    def default(self, o):
        """override the default method to serialize datetime in JSON"""
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return o
