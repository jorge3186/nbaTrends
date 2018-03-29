#!/bin/bash

# start ssh
/usr/sbin/sshd

#reset localhost keys
ssh-keygen -R localhost
ssh-keyscan -H localhost >> ~/.ssh/known_hosts

# start crontab
/usr/sbin/crond


# start jobs
python -m src.scheduler
sleep infinity