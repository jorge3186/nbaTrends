#!/bin/bash

# start ssh
/usr/sbin/sshd

#reset localhost keys
ssh-keygen -R localhost
ssh-keyscan -H localhost >> ~/.ssh/known_hosts

# start crontab
/usr/sbin/crond

# start filebeat
/usr/share/filebeat/filebeat -e -c /usr/share/filebeat/filebeat.yml &

# start jobs
python -m src.scheduler
sleep infinity