#!/bin/bash

# start ssh
service ssh restart

#reset localhost keys
ssh-keygen -R sparkmaster
ssh-keygen -R localhost
ssh-keygen -R 0.0.0.0
ssh-keyscan -H sparkmaster >> ~/.ssh/known_hosts
ssh-keyscan -H localhost >> ~/.ssh/known_hosts
ssh-keyscan -H 0.0.0.0 >> ~/.ssh/known_hosts

# load splunk
/sbin/entrypoint.sh start-and-exit

# start spark
if [ "$1" == "master" ]; then
    /usr/local/spark/sbin/start-master.sh
    /opt/splunkforwarder/bin/splunk add monitor "/usr/local/spark/logs/*.log" -index main -sourcetype spark_logs -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS
elif [ "$1" == "worker" ]; then
    /usr/local/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://sparkmaster:7077
    /opt/splunkforwarder/bin/splunk add monitor "/usr/local/spark/logs/*.log" -index main -sourcetype spark_logs -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS
else
    python3.6 -m src.scheduler
    /opt/splunkforwarder/bin/splunk add monitor "/sbin/nbaTrends/logs/*.log" -index main -sourcetype jobs_logs -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS
fi

/opt/splunkforwarder/bin/splunk add forward-server splunk:9997 -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS

# restart splunk
/opt/splunkforwarder/bin/splunk restart -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS

# hold container open
sleep infinity