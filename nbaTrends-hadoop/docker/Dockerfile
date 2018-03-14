FROM docker.elastic.co/beats/filebeat:6.2.2

USER root

RUN yum clean all; \
    yum install -y curl which tar sudo openssh-server openssh-clients rsync

RUN yum -y update
RUN yum install -y initscripts && yum clean all

# enable ssh
RUN ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN ssh-keygen -N "" -t rsa -f /root/.ssh/id_rsa
RUN cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys
RUN mkdir /var/run/sshd

# Java 1.8
RUN curl -v -j -k -L -O -H 'Cookie: oraclelicense=accept-securebackup-cookie' http://download.oracle.com/otn-pub/java/jdk/8u161-b12/2f38c3b165be4555a1fa6e98c45e0808/jdk-8u161-linux-x64.rpm
RUN rpm -i jdk-8u161-linux-x64.rpm
RUN rm -f jdk-8u161-linux-x64.rpm

ENV JAVA_HOME /usr/java/default
ENV PATH $PATH:$JAVA_HOME/bin
RUN rm -f /usr/bin/java && ln -s $JAVA_HOME/bin/java /usr/bin/java

# Hadoop 3.0.0
RUN curl -v -j -k -L -O 'http://apache.claz.org/hadoop/common/hadoop-3.0.0/hadoop-3.0.0.tar.gz'
RUN tar -xzf hadoop-3.0.0.tar.gz
RUN cp -R hadoop-3.0.0 /usr/local
RUN rm -rf hadoop-3.0.0
RUN rm -f hadoop-3.0.0.tar.gz
RUN cd /usr/local && ln -s ./hadoop-3.0.0 /usr/local/hadoop

RUN mkdir /usr/local/hadoop/hdfs
RUN mkdir /usr/local/hadoop/hdfs/name
RUN mkdir /usr/local/hadoop/hdfs/data

ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_COMMON_HOME /usr/local/hadoop
ENV HADOOP_HDFS_HOME /usr/local/hadoop
ENV HADOOP_MAPRED_HOME /usr/local/hadoop
ENV HADOOP_YARN_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR /usr/local/hadoop/etc/hadoop
ENV HDFS_NAMENODE_USER root
ENV HDFS_DATANODE_USER root
ENV HDFS_SECONDARYNAMENODE_USER root
ENV YARN_NODEMANAGER_USER root
ENV YARN_RESOURCEMANAGER_USER root

ENV PATH $PATH:$HADOOP_HOME/bin

COPY ./core-site.xml $HADOOP_CONF_DIR/core-site.xml
COPY ./hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
COPY ./mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml

COPY ./entrypoint.sh /root
RUN echo "rootroot\nrootroot" | (passwd --stdin root)
RUN chmod +x /root/entrypoint.sh

RUN sed -i 's/# export JAVA_HOME=/export JAVA_HOME=\/usr\/java\/default/' $HADOOP_CONF_DIR/hadoop-env.sh
RUN chmod +x $HADOOP_CONF_DIR/hadoop-env.sh
RUN $HADOOP_CONF_DIR/hadoop-env.sh

# copy filebeat config
COPY ./filebeat.yml /usr/share/filebeat/filebeat.yml
RUN chown root:filebeat /usr/share/filebeat/filebeat.yml

# HDFS Ports
EXPOSE 9820 9864 9865 9866 9867 9869 9870 9871 57199
# Beats
EXPOSE 5044 37978
# ssh port
EXPOSE 22

WORKDIR /root

ENTRYPOINT ["./entrypoint.sh"]
