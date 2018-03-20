# Jobs
Python jobs executed in a docker container and scheduled with crontab.
This application was built using virtualenv. 

### Making Changes
If you wish to make changes, and run the code in a local environment follow these steps:
```bash
python --version # requires python 3 or greater

virtualenv .
pip install -r requirements-<os>.txt
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