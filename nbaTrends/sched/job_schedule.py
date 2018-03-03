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


class JobScheduler(object):

    def only_if_jobs_passed(self, job):
        return self

    def only_if_jobs_failed(self, job):
        return self

    def only_on_days_of_week(self, days):
        return self


JobScheduler()\
    .only_if_jobs_passed('job1')\
    .only_on_days_of_week('m,t,w,th,f')
