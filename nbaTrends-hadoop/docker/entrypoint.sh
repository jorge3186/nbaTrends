#!/bin/bash

# enable ssh for hdfs
service ssh restart

#reset localhost keys
ssh-keygen -R localhost
ssh-keyscan -H localhost >> ~/.ssh/known_hosts

# stop if already running
$HADOOP_PREFIX/sbin/stop-dfs.sh
$HADOOP_PREFIX/sbin/stop-yarn.sh
$HADOOP_PREFIX/sbin/hadoop-daemons.sh stop datanode

if [ "$1" == "master" ]; then 
    # start all hadoop services on master node
    ssh-keygen -R hdfsmaster
    ssh-keygen -R 0.0.0.0
    ssh-keyscan -H hdfsmaster >> ~/.ssh/known_hosts
    ssh-keyscan -H 0.0.0.0 >> ~/.ssh/known_hosts

    echo 'Y' | hdfs namenode -format
    $HADOOP_PREFIX/sbin/start-dfs.sh
    $HADOOP_PREFIX/sbin/start-yarn.sh
else 
    # start slave and connect to master
    ssh-keygen -R hdfsmaster
    ssh-keyscan -H hdfsmaster >> ~/.ssh/known_hosts

    echo 'Y' | hdfs datanode -format
    $HADOOP_PREFIX/sbin/hadoop-daemons.sh --config $HADOOP_CONF_DIR --script hdfs start datanode
fi


# load splunk
/sbin/entrypoint.sh start-and-exit

/opt/splunkforwarder/bin/splunk add forward-server splunk:9997 -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS
/opt/splunkforwarder/bin/splunk add monitor "/usr/local/hadoop/logs/*.log" -index main -sourcetype hadoop_logs -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS
/opt/splunkforwarder/bin/splunk add monitor "/usr/local/hadoop/logs/*.out" -index main -sourcetype hadoop_out -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS

/opt/splunkforwarder/bin/splunk restart -auth "admin:$SPLUNK_PASSWORD" $SPLUNK_START_ARGS

# hold container open
sleep infinity