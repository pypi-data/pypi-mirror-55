# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 13:32
# @E-Mail  : aberstone.hk@gmail.com
# @File    : utils.py
# @Software: PyCharm

# LOGGER
import sys
from loguru import logger

log_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<fg #68be8d>{time:YYYY-MM-DD HH:mm:ss}</> | <fg #68be8d>{level}</> | <fg #68be8d>{message}</>",
            "colorize": True,
            "level": "DEBUG",
            "filter": lambda x: str(x['level']) == "DEBUG"
        },
        {
            "sink": sys.stdout,
            "format": "<fg #80aba9>{time:YYYY-MM-DD HH:mm:ss}</> | <fg #80aba9>{level}</> | <fg #80aba9>{message}</>",
            "colorize": True,
            "level": "INFO",
            "filter": lambda x: str(x['level']) == "INFO"
        },
        {
            "sink": sys.stdout,
            "format": "<fg #ea5506>{time:YYYY-MM-DD HH:mm:ss}</> | <fg #ea5506>{level}</> | <fg #ea5506>{message}</>",
            "colorize": True,
            "level": "WARNING",
            "filter": lambda x: str(x['level']) == "WARNING"
        },
        {
            "sink": sys.stdout,
            "format": "<fg #bf242a>{time:YYYY-MM-DD HH:mm:ss}</> | <fg #bf242a>{level}</> | <fg #bf242a>{message}</>",
            "colorize": True,
            "level": "CRITICAL",
            "filter": lambda x: str(x['level']) == "CRITICAL"
        },
        {
            "sink": sys.stdout,
            "format": "<fg #ffd900>{time:YYYY-MM-DD HH:mm:ss}</> | <fg #ffd900>{level}</> | <fg #ffd900>{message}</>",
            "colorize": True,
            "level": "ERROR",
            "filter": lambda x: str(x['level']) == "ERROR"
        }
    ]
}

logger.configure(**log_config)

LOGGER = logger

