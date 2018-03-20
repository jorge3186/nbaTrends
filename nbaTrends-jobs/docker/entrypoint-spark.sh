#!/bin/bash

# start ssh
/usr/sbin/sshd

# start crontab
/usr/sbin/crond

# start filebeat
/usr/share/filebeat/filebeat -e -c /usr/share/filebeat/filebeat.yml &

# start spark
if [ "$1" == "master" ]; then
    python -m src.scheduler
    sleep infinity
else
    /usr/local/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
fi