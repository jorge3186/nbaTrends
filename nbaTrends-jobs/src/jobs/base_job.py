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

from src.utils import config_utils
from src.utils.logger import get_logger
from src.sched.cronjob import cronjob

from pyspark import SparkConf
from pyspark import SparkContext

logger = get_logger(__name__)

class BaseJob(object):

    def set_name(self, name=None):
        """Sets the Job name in the Spark Context
            By Default the job name is set to the class name
        """
        self.job_name = name

    def pre_run(self, sc):
        """Pre Hook for any necessary setup or executions that need to be done
            prior to job execution.
            :param sc - Spark Context
        """
        pass

    def on_complete(self, sc, success):
        """Post Hook execution for any necessary post conditions that need to be
            applied after a job has been completed.
            :param sc - Spark Context
        """
        pass

    def run(self, sc):
        """Job Execution Step. 
        """
        pass

    def _runjob(self):
        """Internal execution of job"""
        if not hasattr(self, 'job_name'):
            self.job_name = self.__class__.__name__

        logger.info('Starting SparkContext')
        sc = None
        successful = True
        try:
            conf = SparkConf()\
                .setAppName(self.job_name)\
                .setMaster(config_utils.get_config_string('spark_master', 'Spark'))

            sc = SparkContext(conf=conf)

            logger.info('Starting Pre-Execution for job \'%s\'' % (self.job_name))
            self.pre_run(sc)
            logger.info('Pre-Execution for job \'%s\' is complete' % (self.job_name))

            logger.info('Starting job \'%s\'' % (self.job_name))
            self.run(sc)
            logger.info('job \'%s\' has finished' % (self.job_name))
        except Exception as err:
            logger.error('Issue occured during execution')
            logger.error(err.args)
            successful = False
        finally:
            logger.info('Starting Post-Execution for job \'%s\'' % (self.job_name))
            self.on_complete(sc=sc, success=successful)
            logger.info('Post-Execution for job \'%s\' is complete' % (self.job_name))

            if sc is not None:
                sc.stop()
