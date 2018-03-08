#!/usr/bin/env python
"""
    Scraper Job The gathers information from espn.com

    Gather/Parse/Persist Espn information on a daily basis
    and utilize Spark to save data to hdfs file systems.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

from src.utils import config_utils
from src.utils.logger import get_logger
from src.sched.cronjob import cronjob
from src.jobs.base_job import BaseJob

logger = get_logger(__name__)

@cronjob(config='')
class ESPNScrapperJob(BaseJob):

    def run(sc):
        logger.info('Connecting to ESPN.com')