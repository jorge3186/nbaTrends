#!/usr/bin/env python
"""
    Jobs

    Root Package for all Jobs
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

from src.jobs.espn.daily_leaders_job import DailyLeadersJob
from src.jobs.espn.daily_stories_job import DailyStoriesJob

__all__ = [
    # ESPN.com
    "DailyLeadersJob",
    "DailyStoriesJob"

    # NBA.com
]
