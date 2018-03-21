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
import os

class SchedContext(object):

    def __init__(self):
        """Initialize crontab and store in local variable 'cron'"""
        self.cron = CronTab(user=config_utils.get_config_string('user', 'Crontab'))

    def add_job(self, job, create_log=True, sched=None):
        """Add job to the crontab context"""
        cmd = 'spark-submit'
        packages = config_utils.get_config_string('packages', 'Spark')
        if packages is not None:
            cmd += ' --packages %s' % packages

        cmd+= ' /root/nbaTrends/src/main.py ' + job.__name__ 
        if create_log:
            cmd_log = '/var/log/crontab/' + job.__name__ + '.log'
            cmd += ' >> ' + cmd_log

            if not os.path.exists(cmd_log):
                os.makedirs(os.path.dirname(cmd_log))
                with open(cmd_log, 'w+'): pass

        j = self.cron.new(command=cmd)
        j.comment = job.__name__

        if sched is not None:
            sched(j)
        self.cron.write()
        return self

    def remove_job(self, jobname):
        """Remove the current job from
            crontab for the given user
        """
        self.cron.remove_all(comment=jobname)
        return self
