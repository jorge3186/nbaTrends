#!/bin/bash

# start ssh
/usr/sbin/sshd

#reset localhost keys
ssh-keygen -R sparkmaster
ssh-keygen -R localhost
ssh-keygen -R 0.0.0.0
ssh-keyscan -H sparkmaster >> ~/.ssh/known_hosts
ssh-keyscan -H localhost >> ~/.ssh/known_hosts
ssh-keyscan -H 0.0.0.0 >> ~/.ssh/known_hosts

# start crontab
/usr/sbin/crond

# start filebeat
/usr/share/filebeat/filebeat -e -c /usr/share/filebeat/filebeat.yml &

# start spark
if [ "$1" == "master" ]; then
    /usr/local/spark/sbin/start-master.sh
else
    /usr/local/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://sparkmaster:7077
fi

sleep infinity