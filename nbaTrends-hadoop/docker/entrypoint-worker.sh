#!/bin/bash

/usr/sbin/sshd

hdfs datanode -format

hdfs --daemon start datanode

/bin/bash