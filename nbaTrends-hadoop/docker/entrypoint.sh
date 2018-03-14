#!/bin/bash

# enable ssh for hdfs
/usr/sbin/sshd

if [ "$1" == "master" ]; then 
    # start all hadoop services on master node
    hdfs namenode -format
    $HADOOP_HOME/sbin/start-all.sh
else 
    # start slave and connect to master
    hdfs datanode -format
    hdfs --daemon start datanode
fi

# start filebeat
/usr/share/filebeat/filebeat -e -c /usr/share/filebeat/filebeat.yml