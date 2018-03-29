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

from datetime import datetime
import time


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
        time.sleep(8)

        # get stat links
        stat_links = DriverUtil.find_by_xpath(self.driver, \
            '//a[contains(@href, "statistics") and contains(., "Complete Leaders")]')

        links = []
        for lnk in stat_links:
            links.append(lnk.get_attribute('href'))

        for link in links:
            self.driver.get(link)
            logger.info('Navigated to Stat Page: %s' % link)
            time.sleep(5)

            # title row
            stat_names = []
            titles = DriverUtil.find_by_xpath(self.driver, '(//tr[@class="colhead"])[1]//td')
            time.sleep(5)

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
            if 'field' in page_name:
                page_name = 'field_goal_pct'

            logger.info(':::: %s titles before correction ::::' % page_name)
            logger.info(stat_names)

            adjusted_names = AvroUtils.sanitize_field_names(stat_names)
            logger.info(':::: %s titles after correction ::::' % page_name)
            logger.info(adjusted_names)

            if '&nbsp;' not in stat_names:
                stat_data = []
                done = False
                while not done:
                    stat_data += self.get_player_rows()
                    # go to next page
                    next_page_btn = DriverUtil.find_by_xpath(self.driver, '//div[@class="jcarousel-next"]')
                    if len(next_page_btn) > 0:
                        self.driver.execute_script('arguments[0].click()', next_page_btn[0])
                        time.sleep(5)
                    else:
                        done = True

                # create dataframe form stat data then save to hdfs
                stat_df = spark.createDataFrame(stat_data, adjusted_names)
                AvroUtils.avro_to_hdfs(stat_df, '/stats/leaders/' + page_name)


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
                el_text = el.get_attribute('innerHTML')
                if '<a' in el_text:
                    el_text = DriverUtil.find_by_xpath(el, './/a')[0].get_attribute('innerHTML')

                r.append(str(el_text).replace('&nbsp;', ''))
            r.append(datetime.now().strftime('%Y-%m-%d'))
            data_rows.append(r)
        self.fix_rank_ties(data_rows)
        return data_rows


    def fix_rank_ties(self, data_rows):
        """
            Iterate through the player rows, looking for empty ranks.
            If an empty rank is found then it gets the previous row's rank
            and marks it that same rank prefixed with 'T-'
        """
        prev_rank = None
        for i, row in enumerate(data_rows):
            if '' == row[0] and prev_rank is not None:
                row[0] = data_rows[i-1][0]
                if 'T-' not in row[0]:
                    row[0] = 'T-' + row[0]
                    data_rows[i-1][0] = row[0]
            prev_rank = row[0]

