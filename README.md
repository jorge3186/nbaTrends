# NBA Trends
This is a docker service that will use web-scraper jobs to pick up various NBA Information from popular websites and place them in a Hadoop file system (HDFS). Once populated, ETL jobs are then used to save  that data to a Mongo db which is used by a vue.js Front End application to display the current trends and projected changes in the NBA on a daily basis.


This docker swarm sends all logs to a splunk instance that you can visit at port 31000. The swarm consists of at minimum 8 containers.
- Splunk Enterprise Instance
- Hadoop Master Node
- Hadoop Worker Node (can be scaled)
- Spark Master Node
- Spark Worker Node (can be scaled)
- Job Executable Container
- MongoDB instance
- Apache Httpd instance for UI


The goal is to have these re-occuring jobs that scrape the web for data, save that data to avro files through hdfs and then these files will be ultimately used to extract information that will be displayed through a UI.

### Getting Started
- Ensure docker is installed
- [Create networks](#network-setup)
- [Build](#build-compose)

    ### Network Setup
    This network needs to be created before building
    - hadoop

    The network can either be <strong>bridge</strong> or <strong>overlay</strong> networks based on your docker swarm configuration.
    Examples: 
    ```bash
    docker network create -d bridge hadoop
    docker network create -d overlay hadoop
    ```

    ### Build Compose
    Once networks have been created just run the following commands:
    ```bash
    cd ./docker
    docker-compose up
    #or
    docker stack deploy -c ./docker-stack.yml nbaTrends
    ```
