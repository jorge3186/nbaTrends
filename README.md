# NBA Trends
This is a docker service that will user web-scraper jobs to pick up various NBA Information from popular websites and place them in a Hadoop file system (HDFS). Once populated, ETL jobs are then used to save to that data to a MySQL db which is used by an angular application to display the current trends in the NBA on a daily basis.

### Getting Started
- Ensure docker is installed
- [Create networks](#network-setup)
- [Build](#compose)

#### Network Setup
These 3 networks need to be created before building
- elasticsearch
- hadoop
- spark

These networks can either be bridge or overlay networks based on your docker swarm configuration.
Examples: 
- `docker network create -d bridge elasticsearch`
- `docker network create -d overlay hadoop`

### Compose
Once networks have been created just run the following commands:
```
cd ./docker
docker-compose up
```