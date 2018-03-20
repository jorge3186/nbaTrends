#!/usr/bin/env python
"""
    Main File for Executing Spark Jobs
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

import subprocess
import sys

if __name__ == "__main__":
    """
        Execute the specified job within the module provided.
    """
    subprocess.call(['python', '-m', 'src.executor', sys.argv[1]], cwd='/root/nbaTrends')