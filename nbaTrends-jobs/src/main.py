#!/usr/bin/env python
"""
    Main File for NBA Trends

    Starts the application and configures Crontab with all
    available jobs.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

import src.jobs as jobs
from src.sched.sched_context import SchedContext

if __name__ == "__main__":
    """
        Gather all jobs from job context and setup crontab
        
        By Instansiating the class object, The Crontab Context 
        will be updated to create/update job context
    """
    for job in jobs.__all__:
        j = getattr(jobs, job)
        j()

