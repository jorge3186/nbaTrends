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

import os

logger = get_logger(__name__)


def cronjob(set_job):
    """
    Add a Job to the crontab scheduler. 
    Provide a lambda function that will set 
    job scheduling attributes.
    """
    def real_decorator(job):
        """Get Crontab Context and add job
        """
        try:
            sched_context = SchedContext()
            cron = sched_context.cron
            cron.remove_all(comment=job.__name__)

            cmd = 'spark-submit /root/nbaTrends/src/main.py ' + job.__name__ 
            cmd_log = '/var/log/crontab/' + job.__name__ + '.log'
            cmd += ' >> ' + cmd_log

            if not os.path.exists(cmd_log):
                os.makedirs(os.path.dirname(cmd_log))
                with open(cmd_log, 'w+'): pass

            cjob = cron.new(command=cmd)
            cjob.comment = str(job.__name__)
            set_job(cjob)
            cron.write()
        except Exception as err:
            logger.error('Error initializing Crontab.')
            logger.error(err.args)
        return job
    return real_decorator
        