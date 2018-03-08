#!/usr/bin/env python
"""
    Sched Context

    A context that provides an easy builder to set up the
    scheduling for the given job. This includes the time schedule
    and pre-conditions.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

from src.utils import config_utils
from crontab import CronTab


class SchedContext(object):

    def __init__(self):
        self.cron = CronTab(user=config_utils.get_config_string('user', 'Crontab'))

    def add_job(self, job, sched):
        return self

    def get_job_sched(self, job):
        return self

    def has_job(self, job):

        return False
