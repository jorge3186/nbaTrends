#!/usr/bin/env python
"""
    Scraper Job The gathers stat leaders
    from espn.com on a daily basis

    Job Schedule: 
        Every day
        at 1:00 AM
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
from src.utils.avro_utils import AvroUtils

from pyspark.sql import *
from pyspark.sql.types import *
from datetime import datetime


logger = get_logger(__name__)

@cronjob(lambda job: (\
    job.hour.on(1),\
    job.minute.on(0)))
class DailyLeadersJob(SeleniumJob):

    def run(self, spark):
        """
            Navigate to the statistics page for nba players.
            For each statistic gather the list and statistics info and
            store into an avro file that will be labeled based on date
            and statistic name.

            :param: spark - the SparkSession generated by BaseJob
        """
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
                el_text = title.get_attribute('innerHTML')
                if '<a' in el_text:
                    el_text = DriverUtil.find_by_xpath(title, './/a')[0].get_attribute('innerHTML')
                elif '<span' in el_text:
                    el_text = DriverUtil.find_by_xpath(title, './/span')[0].get_attribute('innerHTML')
                stat_names.append(el_text)
            
            title_el = DriverUtil.find_by_xpath(self.driver, '//div[@class="mod-header stathead"]/h4')[0]\
                .get_attribute('innerHTML')

            # add date field to headers
            stat_names.append('date')
            page_name = str(title_el).split(' ')[0].lower()
            logger.info(':::: %s titles ::::' % page_name)
            logger.info(stat_names)

            stat_data = []
            done = False
            while not done:
                stat_data += self.get_player_rows()
                # go to next page
                next_page_btn = DriverUtil.find_by_xpath(self.driver, '//div[@class="jcarousel-next"]')
                if len(next_page_btn) > 0:
                    next_page_btn[0].click()
                else:
                    done = True

            # create dataframe form stat data then save to hdfs
            stat_df = spark.createDataFrame(stat_data, stat_names)
            AvroUtils.avro_to_hdfs(stat_df, '/stats/leaders/'.join([page_name, '.avro']))

    def get_player_rows(self):
        """
            Get all rows with player stats.
            Add an additional column to store today's date.

            :return: rows of player data  
        """
        data_rows = []
        player_rows = DriverUtil.find_by_xpath(self.driver, '//tr[contains(@class, "player")]')
        for row in player_rows:
            r = []
            for el in DriverUtil.find_by_xpath(row, './/td'):
                if len(DriverUtil.find_by_xpath(el, './/a[contains(@href, "/nba/player")]')) > 0:
                    val = DriverUtil.find_by_xpath(el, './/a[contains(@href, "/nba/player")]')[0]\
                        .get_attribute('innerHTML')
                    r.append(val)
                else:
                    r.append(DriverUtil.find_by_xpath(row, './/td'))[0].get_attribute('innerHTML')
            r.append(datetime.now().strftime('%Y-%m-%d'))
            data_rows.append(r)
        return data_rows
