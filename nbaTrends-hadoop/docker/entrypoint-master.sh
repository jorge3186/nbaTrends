#!/bin/bash

/usr/sbin/sshd

hdfs namenode -format

$HADOOP_HOME/sbin/start-all.sh

/bin/bash