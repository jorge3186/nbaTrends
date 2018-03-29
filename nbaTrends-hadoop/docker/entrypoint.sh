#!/bin/bash

# enable ssh for hdfs
/usr/sbin/sshd

#reset localhost keys
ssh-keygen -R localhost
ssh-keyscan -H localhost >> ~/.ssh/known_hosts

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

sleep infinity
