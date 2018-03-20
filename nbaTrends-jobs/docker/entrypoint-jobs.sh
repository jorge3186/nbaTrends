#!/bin/bash

# start ssh
/usr/sbin/sshd

# start crontab
/usr/sbin/crond

# start filebeat
/usr/share/filebeat/filebeat -e -c /usr/share/filebeat/filebeat.yml &

# start jobs
python -m src.scheduler
sleep infinity