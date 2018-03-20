# Jobs
Python jobs executed in a docker container and scheduled with crontab.
Using PySpark, jobs are executed in Apache Spark to fetch and transform data on a daily
basis for the Current Trends in the NBA.

### Making Changes
If you wish to make changes, and run the code in a local environment follow these steps:
```bash
python --version # prefer python 3 or greater

virtualenv .
pip install -r requirements.txt
source ./bin/activate
# or on windows
./Srcipts/activate.bat
```

### Running Jobs
```bash
python -m src.scheduler # will add jobs to crontab

# or if you want to execute a specific job manually
python -m src.executor <job_name> # job name is the python class that extends BaseJob
```