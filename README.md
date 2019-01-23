# NBA Trends
This is a docker service that will use web-scraper jobs to pick up various NBA Information from popular websites and place them in a Hadoop file system (HDFS). Once populated, ETL jobs are then used to save to that data to a MySQL db which is used by an angular application to display the current trends in the NBA on a daily basis.

### Getting Started
- Ensure docker is installed
- [Create networks](#network-setup)
- [Build](#build-compose)

    ### Network Setup
    This network needs to be created before building
	- splunk
    - hadoop

    The network can either be <strong>bridge</strong> or <strong>overlay</strong> networks based on your docker swarm configuration.
    Examples: 
    ```bash
    docker network create -d bridge splunk
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
