#!/bin/bash

# start crontab
service crond start

cd /root
python -m nbaTrends.scheduler