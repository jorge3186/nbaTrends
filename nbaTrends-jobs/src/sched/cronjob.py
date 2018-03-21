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
from src.sched.sched_context import SchedContext

logger = get_logger(__name__)


def cronjob(schedule=None):
    """
    Add a Job to the crontab scheduler. 
    Provide a lambda function that will set 
    job scheduling attributes.

    By default, when no schedule is provided the job
    is set to run every minute of every day.
    """
    def real_decorator(job):
        """Get Crontab Context and add job"""
        try:
            SchedContext() \
                .remove_job(job.__name__) \
                .add_job(job, sched=schedule)
        except Exception as err:
            logger.error('Error initializing Crontab.')
            logger.error(err.args)
        return job
    return real_decorator
        