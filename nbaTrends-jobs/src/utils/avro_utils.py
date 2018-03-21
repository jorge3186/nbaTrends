#!/usr/bin/env python
"""
    Avro Utility for read/write of avro files and schemas.

    This utiltiy also can be used in conjunction with SparkContext
    and parallization of RDDs and DataFrames.
"""

__author__ = "Jordan Alphonso"
__copyright__ = "Copyright 2018, jordanalphonso.net"
__credits__ = ["Jordan Alphonso"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jordan Alphonso"
__email__ = "jordanalphonso1@yahoo.com"

from src.utils import config_utils

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import json
from datetime import datetime

class AvroUtils(object):

    @staticmethod
    def create_schema(name, fields, schema_type='record'):
        """
            Create an Avro schema 

            :param: name - The schema name including the class name
            :param: schema_type - The type of avro file, default is record
            :param: fields - The fields to include in schema
            :return: the generated schema
        """
        pre_schema = {'type': schema_type} 
        pre_schema['name'] = str(name).split('.')[len(str(name).split('.'))-1]
        pre_schema['namespace'] = name.replace(name.split('.')[len(name.split('.'))-1], '')[:-1]
        pre_schema['fields'] = []
        for field in fields:
            if isinstance(field, str):
                pre_schema['fields'].append({'name':field, 'type':['string', 'null']})
            elif hasattr(field, 'type'):
                pre_schema['fields'].append({'name':field.get('name'), 'type': field.get('type')})
        return avro.schema.Parse(json.dumps(obj))

    @staticmethod
    def avro_to_hdfs(df, file_path, append_timestamp=True):
        """
            Write spark dataframe to avro file.

            :param: df - dataframe to convert to .avro file
            :param: file_path - the location in which to store the file
            :param: append_timestamp - Add timestamp to filename. Default is True
                Format is %Y%m%d%H%M%S
        """
        if append_timestamp:
            ts = datetime.no().strftime('%Y%m%d%H%M%S')
            file_path = str(file_path).replace('.avro', '.'.join([ts, '.avro']))

        df.write.format('com.databricks.spark.avro').save(\
            config_utils.get_config_string('hdfs_home', 'Hadoop') + file_path)