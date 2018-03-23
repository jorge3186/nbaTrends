#!/usr/bin/env python
"""
    Scraper Job The gathers front page
    stories from the /nba url and packages 
    them into an avro.
    
    Job Schedule: 
        Every Day
        at 12:00 PM, 3:00 PM, 8:00 PM, 12:00 AM
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"

from src.jobs.selenium_job import SeleniumJob
from src.sched.cronjob import cronjob
from src.utils.logger import get_logger
from src.utils.webdriver_util import get_driver
from src.utils.webdriver_util import DriverUtil

from datetime import datetime


logger = get_logger(__name__)

@cronjob(lambda job: (\
    job.hour.on(0,12,15,20),\
    job.minute.on(0)))
class DailyStoriesJob(SeleniumJob):

    def run(self, spark):
        """
            Navigate to espn.com/nba front page and gather the
            headline stories 1 by 1 and store them in an avro
            file based on the 
        """
        self.driver.get('http://espn.com/nba')
        logger.info('Navigated to espn.com/nba')

        
