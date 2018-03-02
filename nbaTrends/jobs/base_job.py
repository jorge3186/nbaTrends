#!/usr/bin/env python
"""
    Base class for creating a spark job.

    SparkContext will be initialized and can
    be accessed using 'sc'.

"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

from nbaTrends.utils import config_utils

from pyspark import SparkConf
from pyspark import SparkContext


class BaseJob(object):

    def __init__(self, job_name):
        """Constructor To initialize a base spark job.
            A SparkContext will be accessible as 'sc'.

            :param job_name - The name that will be given to the SparkContext.
        """
        self.conf = SparkConf()\
            .setAppName(job_name)\
            .setMaster(config_utils.get_config_string('spark_master', section='Spark'))

        self.sc = SparkContext(self.conf)

    def sched(self, crontab_str=None):
        pass