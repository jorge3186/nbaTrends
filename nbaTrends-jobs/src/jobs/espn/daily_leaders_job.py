#!/usr/bin/env python
"""
    Scraper Job The gathers leaders information
    from espn.com on a daily basis
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"

from src.jobs.base_job import BaseJob
from src.sched.cronjob import cronjob
from src.utils.logger import get_logger
from src.utils.webdriver_util import get_driver
from src.utils.webdriver_util import DriverUtil
from src.utils.avro_utils import AvroUtils

from pyspark.sql import *
from pyspark.sql.types import *


logger = get_logger(__name__)

@cronjob(lambda job: (\
    job.hour.on(1),\
    job.minute.on(0)))
class DailyLeadersJob(BaseJob):

    def pre_run(self, spark):
        """Initialize Selenium Webdriver"""
        self.driver = get_driver()

    def run(self, spark):
        """ Execute job"""
        self.driver.get('http://espn.com/nba/statistics')
        logger.info('Navigated to espn.com/nba/statistics')

        # get stat links
        stat_links = DriverUtil.find_by_xpath(self.driver, \
            '//a[contains(@href, "statistics") and contains(., "Complete Leaders")]')

        links = []
        for lnk in stat_links:
            links.append(lnk.get_attribute('href'))

        for link in links:
            self.driver.get(link)
            logger.info('Navigated to Stat: %s' % link)

            # title row
            stat_names = []
            titles = DriverUtil.find_by_xpath(self.driver, '(//tr[@class="colhead"])[1]//td')
            for title in titles:
                if DriverUtil.find_by_xpath(title, '//a[contains(@href, "statistics")]') is not None:
                    inner_el = DriverUtil.find_by_xpath(title, '//a[contains(@href, "statistics")]')
                    title_names.append(inner_el.get_attribute('innerHTML'))
                else:
                    title_names.append(title.get_attribute('innerHTML'))
            logger.info('Titles: ' + title_names)
            title_el = DriverUtil.find_by_xpath(self.driver, '//div[@class="mod-header stathead"]/h4')[0]\
                .get_attribute('innerHTML')

            page_name = str(title_el).split(' ')[0].lower()

            stat_data = []
            done = False
            while not done:
                stat_data += self.get_player_rows()
                # go to next page
                next_page_btn = DriverUtil.find_by_xpath(self.driver, '//div[@class="jcarousel-next"]')
                if next_page_btn is not None:
                    next_page_btn.click()
                else:
                    done = True

            # create dataframe form stat data
            stat_df = spark.createDataFrame(stat_data, stat_names)
            AvroUtils.avro_to_hdfs(stat_df, '/stats/leaders/'.join([page_name, '.avro']))


    def on_complete(self, sc, success):
        """Clean up webdriver when finished"""
        if success:
            logger.info('Successfully collected leader data from espn.com')
        else:
            logger.error('Issue while collecting leader data from espn.com')
        self.driver.close()
        logger.info('Closing webdriver and cleaning up job context.')


    def get_player_rows(self):
        """
            Get all rows with player stats

            :return: rows of player data    
        """
        data_rows = []
        player_rows = DriverUtil.find_by_xpath(self.driver, '//tr[contains(@class, "player")]')
        for row in player_rows:
            r = []
            for el in DriverUtil.find_by_xpath(row, '//td'):
                if DriverUtil.find_by_xpath(el, '//a[contains(@href, "/nba/player")]') is not None:
                    val = DriverUtil.find_by_xpath(el, '//a[contains(@href, "/nba/player")]')[0]\
                        .get_attribute('innerHTML')
                    r.append(val)
                else:
                    r.append(DriverUtil.find_by_xpath(row, '//td'))[0].get_attribute('innerHTML')
            data_rows.append(r)
        return data_rows
