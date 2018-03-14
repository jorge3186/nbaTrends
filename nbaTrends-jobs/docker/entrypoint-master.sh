#!/bin/bash

# start crontab
service crond start

# install dependencies with pip
cd /root/nbaTrends
pip install -r requirements-linux.txt

# schedule cron jobs
python -m src.scheduler