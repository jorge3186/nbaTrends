#!/usr/bin/env python
"""
    A Base job that will use selenium webdriver
    and webdriver utils.
    For convenience, so we don't always have to initialize 
    a webdriver in every job that wants to use one.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"

from src.jobs.base_job import BaseJob
from src.utils.webdriver_util import get_driver()
from src.utils.logger import get_logger


logger = get_logger(__name__)

class SeleniumJob(BaseJob):

    def pre_run(self, spark):
        """
            Initialize a webdriver and store it as self.driver

            :param: spark - the SparkSession generated in BaseJob
            :returns: True if the webdriver was successfully created, False 
                if there were issues initializing the driver
        """
        try:
            self.driver = get_driver()
            return True
        except Exception as err:
            logger.error(err.args)
            return False

    def on_complete(self, spark, success):
        """
            Clean up webdriver and close context

            :param: spark - the SparkSession generated in BaseJob
            :param: success - a bool that signifies if there was an exception
                thrown during job execution. If an exception occurs, then success
                is False
        """
        if self.driver is not None:
            logger.info('Closing webdriver')
            self.driver.close()