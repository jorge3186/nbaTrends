#!/usr/bin/env python
"""
    @cronjob

    Decorator for assigning spark jobs with a schedule
    configuration
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

from src.utils.logger import get_logger

logger = get_logger(__name__)

def cronjob(**config):
    """Decorator that wraps a class instance with cron config
    """
    def real_decorator(job):
        def wrapper(*args, **kwargs):
            pass
        return job
    return real_decorator
        