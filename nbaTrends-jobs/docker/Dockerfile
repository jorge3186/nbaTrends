FROM splunk/universalforwarder:7.2

USER root

RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list
RUN apt-get update
RUN mkdir /usr/share/man/man1
RUN apt-get install openssh-server curl wget zlib1g-dev cmake -y
RUN apt-get install build-essential checkinstall -y
RUN apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev -y
RUN apt-get install tk-dev libgdbm-dev libc6-dev libbz2-dev -y

RUN echo y | ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
RUN echo y | ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN echo y | ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
RUN cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# Python 3.6
RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
RUN tar xvf Python-3.6.3.tgz
WORKDIR ./Python-3.6.3
RUN ./configure --enable-optimizations
RUN make
RUN make altinstall
RUN python3.6 -m pip install --upgrade pip
RUN ln -sfn /usr/local/bin/python3.6 /usr/bin/python3.6

# Crontab 
RUN apt-get install cron -y

# Java 1.8
RUN apt-get install openjdk-8-jdk -y

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $PATH:$JAVA_HOME/bin
RUN rm -f /usr/bin/java && ln -s $JAVA_HOME/bin/java /usr/bin/java

# Spark 2.4 / Hadoop 2.7
RUN curl -v -j -k -L -O 'http://apache.claz.org/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz'
RUN tar -xzf spark-2.4.0-bin-hadoop2.7.tgz
RUN cp -R spark-2.4.0-bin-hadoop2.7 /usr/local
RUN rm -rf spark-2.4.0-bin-hadoop2.7
RUN rm -f spark-2.4.0-bin-hadoop2.7.tgz
RUN cd /usr/local && ln -s ./spark-2.4.0-bin-hadoop2.7 /usr/local/spark
COPY ./docker/log4j.properties /usr/local/spark/conf/log4j.properties
ENV PATH $PATH:/usr/local/spark/bin

# Avro 1.8.2
RUN curl -v -j -k -L -O 'http://apache.claz.org/avro/avro-1.8.2/py3/avro-python3-1.8.2.tar.gz'
RUN tar -xzf avro-python3-1.8.2.tar.gz
RUN cp -R avro-python3-1.8.2 /usr/local
RUN rm -rf avro-python3-1.8.2
RUN rm -f avro-python3-1.8.2.tar.gz
RUN cd /usr/local && ln -s ./avro-python3-1.8.2 /usr/local/avro
RUN cd /usr/local/avro && python3.6 setup.py install

# chrome
RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub
RUN apt-get update
RUN apt-get install google-chrome-stable -y

RUN apt-get install unzip -y
RUN CHROME_DRIVER_VERSION=`curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
	curl -v -j -k -L -O https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /opt/chromedriver
RUN ln -s /opt/chromedriver/chromedriver /usr/bin/chromedriver

RUN mkdir /root/scripts
COPY ./docker/entrypoint.sh /root/scripts/entrypoint.sh
RUN chmod +x /root/scripts/entrypoint.sh

RUN mkdir /sbin/nbaTrends
RUN mkdir /sbin/nbaTrends/src
ADD ./src /sbin/nbaTrends/src
ADD ./requirements.txt /sbin/nbaTrends
RUN python3.6 -m pip install -r /sbin/nbaTrends/requirements.txt
ENV PYSPARK_PYTHON /usr/bin/python3.6

WORKDIR /sbin/nbaTrends

# spark ports
EXPOSE 8080 7077

ENTRYPOINT ["/root/scripts/entrypoint.sh"]