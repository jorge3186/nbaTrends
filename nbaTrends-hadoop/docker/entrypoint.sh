#!/bin/bash

# enable ssh for hdfs
/usr/sbin/sshd

if [ "$1" == "master" ]; then 
    # start all hadoop services on master node
    hdfs namenode -format
    $HADOOP_HOME/sbin/start-all.sh
    sleep infinity
else 
    # start slave and connect to master
    hdfs datanode -format
    hdfs --daemon start datanode
    sleep infinity
fi