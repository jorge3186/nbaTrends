#!/usr/bin/env python
"""
    Logging Setup for the Application
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

import logging
import os

log_path = os.path.dirname(os.path.realpath(__file__)) + '/../../logs/nbaTrends.log'
if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))
if not os.path.exists(log_path):
    l = open(log_path, "w+")
    l.close()

formatter = logging.Formatter('[[ %(asctime)s :: %(funcName)s@%(filename)s:%(lineno)d :: %(levelname)-5.5s]] %(message)s')

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

def get_logger(name=None):
    """Create a logger based on py filename
        Default Log Level is INFO.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger