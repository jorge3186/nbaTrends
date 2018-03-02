#!/usr/bin/env python
"""
    Configuration Utility for accessing Conf Properties

    Conf properties can be added in resources/config.ini.
    Convenience functions to access a specific conf item
    based on type.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

import ConfigParser
import os

config_file_path = os.path.dirname(os.path.realpath(__file__)) + '/../resources/config.ini'

conf = ConfigParser.ConfigParser()
conf.read(config_file_path)

conf_map = {}


def _init_conf():
    """Loads all sections from config.ini into the
        conf_map dict.
    """
    sections = conf.sections()
    for sec in sections:
        opts_map = {}
        for opt in conf.options(sec):
            try:
                opts_map[opt] = conf.get(sec, opt)
            except:
                pass  # when there is an issue, we simply just skip the item
        conf_map[sec] = opts_map


def get_config_string(name, section=None):
    """Get a config attribute as a str

        :param name - Name of Config Item
        :param section - Name of the section where the config item exists
        :returns str value or None
    """
    if len(conf_map) == 0:
        _init_conf()
    return get_config_item(name, str, section)


def get_config_bool(name, section=None):
    """Get a config attribute as a bool

        :param name - Name of Config Item
        :param section - Name of the section where the config item exists
        :returns bool false or None
    """
    if len(conf_map) == 0:
        _init_conf()
    return get_config_item(name, bool, section)


def get_config_int(name, section=None):
    """Get a config attribute as a int

        :param name - Name of Config Item
        :param section - Name of the section where the config item exists
        :returns int value or None
    """
    if len(conf_map) == 0:
        _init_conf()
    return get_config_item(name, int, section)


def get_config_float(name, section=None):
    """Get a config attribute as a float

        :param name - Name of Config Item
        :param section - Name of the section where the config item exists
        :returns float value or None
    """
    if len(conf_map) == 0:
        _init_conf()
    return get_config_item(name, float, section)


def get_config_item(name, type=str, section=None):
    """Get a config attribute. By default, if no type is passed
        then it will be returned as a str.

        :param name - Name of Config Item
        :param type - type of value to return
        :param section - Name of the section where the config item exists
        :return value of specified type or None
    """
    if len(conf_map) == 0:
        _init_conf()

    if section is None:
        for k, sec in conf_map.items():
            for nme, opt in sec.items():
                if nme == name:
                    return type(opt)
    else:
        for item in conf_map[section]:
            if item == name:
                return type(conf.get(section, item))
    return None


