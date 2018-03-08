#!/usr/bin/env python
"""
    Main File for Executing Spark Jobs
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

import src.jobs as jobs_module
from src.utils.logger import get_logger

import sys

logger = get_logger(__name__)

if __name__ == "__main__":
    job_name = sys.argv[1]
    current_job = None
    for job in jobs_module.__all__:
        if job_name == job:
            current_job = getattr(jobs_module, job_name)
            break
    
    if current_job is not None:
        current_job()._runjob()
    else:
        logger.info('No job with name \'%s\' found. Skipping Execution.' % (job_name))
        logger.info('Be sure the job is registered in the jobs package.')