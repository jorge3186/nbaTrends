#!/usr/bin/env python
"""
    Base class for creating a spark job.

    When creating a new Spark Job, be sure to extend BaseJob
    or one of the BaseJob's child classes.

    Jobs will be named after the class '__name__' attribute unless manually
    specified by calling job.set_name(name='job name').

    A SparkSession will be generated and passed 
    into each method as 'spark' to access the current session, context,
    sql context, etc. Use this session to load/save data, control parallelism,
    execute sql queries and create/manipulate dataframes.

    If any pre conditions need to be met before execution, override the 
    'pre_run' method and return a bool based on whether the job should be executed
    or not.

    If any additional steps are needed after a job is complete, override the
    'on_complete' method.
    
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

from pyspark.sql import SparkSession

logger = get_logger(__name__)

class BaseJob(object):

    def set_name(self, name=None):
        """
            Sets the Job name in the Spark Context
            By Default the job name is set to the class name

            :param: name - The Job name. If not overriden, job name 
                will be class __name__ attribute.
        """
        self.job_name = name

    def pre_run(self, spark):
        """
            Pre Hook for any necessary setup or executions that need to be done
            prior to job execution.

            :param: spark - the generated SparkSession
            :returns: a bool that will determine whether job should be executed.
        """
        return True

    def on_complete(self, spark, success):
        """Post Hook execution for any necessary post conditions that need to be
            applied after a job has been completed.

            :param: spark - the generated SparkSession
            :param: success - a bool that signifies if there was an exception
                thrown during job execution. If an exception occurs, then success
                is False
        """
        pass

    def run(self, spark):
        """
            Job Execution Step. 
            Override this method in Job class
        """
        pass

    def _runjob(self):
        """Internal execution of job"""
        exit_code = 0
        if not hasattr(self, 'job_name'):
            self.job_name = self.__class__.__name__

        logger.info('Starting SparkSession')
        spark = None
        successful = True
        try:
            spark = SparkSession.builder\
                .master(config_utils.get_config_string('spark_master', 'Spark'))\
                .appName(self.job_name)\
                .config(key='spark.sql.avro.compression.codec',\
                    value=config_utils.get_config_string('compression', 'Avro'))\
                .config(key='spark.sql.avro.deflate.level',\
                    value=config_utils.get_config_string('compression_level', 'Avro'))\
                .getOrCreate()

            logger.info('Starting Pre-Execution for job \'%s\'' % (self.job_name))
            should_run = self.pre_run(spark)
            logger.info('Pre-Execution for job \'%s\' is complete' % (self.job_name))

            if should_run is not None and should_run == False:
                logger.info('Pre-run did not end successfully.')
                logger.info('Skipping job execution.')
                raise Exception('Pre-run did not end successfully.')
            else:
                logger.info('Starting job \'%s\'' % (self.job_name))
                self.run(spark)
                logger.info('job \'%s\' has finished' % (self.job_name))           
        
        except Exception as err:
            logger.error('Issue occured during execution')
            logger.error(err.args)
            successful = False
            exit_code = 1
        finally:
            logger.info('Starting Post-Execution for job \'%s\'' % (self.job_name))
            self.on_complete(spark=spark, success=successful)
            logger.info('Post-Execution for job \'%s\' is complete' % (self.job_name))

            if spark is not None:
                spark.stop()
            exit(exit_code)
