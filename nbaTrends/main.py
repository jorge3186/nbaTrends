#!/usr/bin/env python
"""
    Main File for NBA Trends

    Start the application and configures Crontab with all
    available jobs.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

import nbaTrends.jobs as jobs
from nbaTrends.sched.sched_context import SchedContext

job_files = []

def main():
    """
        Gather all jobs from job context and setup crontab
    """
    sched = SchedContext()
    for job in jobs.__all__:
        j = getattr(jobs, job)
        job_instance = j()
        sched.add_job(job_instance, "")


if __name__ == "__main__":
    main()
