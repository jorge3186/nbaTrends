#!/bin/bash

curl -v -j -k -L -O 'http://apache.claz.org/avro/avro-1.8.2/py3/avro-python3-1.8.2.tar.gz'
tar -xzf avro-python3-1.8.2.tar.gz
python ./avro-python3-1.8.2/setup.py install

python -m unittest discover nbaTrends-jobs