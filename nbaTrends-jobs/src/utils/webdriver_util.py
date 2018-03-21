#!/usr/bin/env python
"""
    WebDriver utility for selenium.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"

from src.utils.config_utils import get_config_string

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_driver():
    """
        Create a webdriver using chrome and
        chromedriver.
    """
    opts = Options()
    opts.add_argument('--headless')
    return webdriver.Chrome(chrome_options=opts,\
        executable_path=get_config_string('chromedriver_path', 'Selenium'))


class DriverUtil(object):


    @staticmethod
    def find_by_xpath(driver, xpath):
        """
            Get all elements that match the given
            xpath
        """
        return driver.find_elements(By.XPATH, xpath)


    @staticmethod
    def find_by_id(driver, id):
        """
            Get the element with the given id.
        """
        return driver.find_element(By.ID, id)


    @staticmethod
    def find_by_class(driver, clz):
        """
            Get all elements that match the given
            class name
        """
        return driver.find_elements(By.CLASS_NAME, clz)


    @staticmethod
    def find_by_xpath(driver, xpath):
        """
            Get all elements that match the given
            xpath
        """
        return driver.find_elements(By.XPATH, xpath)
    