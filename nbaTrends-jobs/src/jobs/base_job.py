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

    def pre_exec(self, sc):
        """Pre Hook for any necessary setup or executions that need to be done
            prior to job execution.
        """
        pass

    def post_exec(self, sc, job_success):
        """Post Hook execution for any necessary post conditions that need to be
            applied after a job has been completed.
            :param job_success - If the job was a success or not
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
        try:
            conf = SparkConf()\
                .setAppName(self.job_name)\
                .setMaster(config_utils.get_config_string('spark_master', 'Spark'))

            sc = SparkContext(conf=conf)

            logger.info('Starting Pre-Execution for job \'%s\'' % (self.job_name))
            self.pre_exec(sc)
            logger.info('Pre-Execution for job \'%s\' is complete' % (self.job_name))

            logger.info('Starting job \'%s\'' % (self.job_name))
            run(sc)
            logger.info('job \'%s\' has finished' % (self.job_name))

            logger.info('Starting Post-Execution for job \'%s\'' % (self.job_name))
            post_exec(sc, job_success=True)
            logger.info('Post-Execution for job \'%s\' is complete' % (self.job_name))
        except:
            logger.error('Issue occured during execution')
        finally:
            if sc is not None:
                sc.stop()
