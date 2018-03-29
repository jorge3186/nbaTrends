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
from src.utils.logger import get_logger

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import json
from datetime import datetime
import re

logger = get_logger(__name__)

digit_converter = {
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
    '0': 'zero'
}

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
            If only a directory is passed, then it will by default create a 
            file with the timestamp as name.
            Ex: 
                AvroUtils.avro_to_hdfs(df, '/tmp/example/')
                result - hdfs://host:port/tmp/example/20180329123022.avro

            If a full file path is passed and the append_timestamp is set to True,
            then a timestamp will be appended to the end of the filename.
            Ex:
                AvroUtils.avro_to_hdfs(df, '/tmp/example.avro', append_timestamp=True)
                result - hdfs://host:port/tmp/examples_20180329123022.avro

            :param: df - dataframe to convert to .avro file
            :param: file_path - the location in which to store the file
            :param: append_timestamp - Add timestamp to filename. Default is True
                Format is %Y%m%d%H%M%S
        """
        ts = datetime.now().strftime('%Y%m%d%H%M%S')
        if append_timestamp:
            if str(file_path).endswith('.avro'):
                file_path = str(file_path).replace('.avro', ('_' + ts + '.avro'))
            else:
                if not str(file_path).endswith('/'):
                    file_path = file_path + '/'
                file_path = file_path + ts + '.avro'
        elif not str(file_path).endswith('.avro'):
            if not str(file_path).endswith('/'):
                file_path = file_path + '/'
            file_path = file_path + ts + '.avro'

        f = config_utils.get_config_string('hdfs_home', 'Hadoop') + file_path
        logger.info('Saving HDFS Avro File :: %s' % f)
        df.write.format('com.databricks.spark.avro').save(f)
        logger.info('Avro file save complete')


    @staticmethod
    def sanitize_field_names(field_names):
        """
            Checks each field name for invalid characters.
            Avro field names should conform to the following
            regex:
                Start with [A-Za-z_]
                Contains only [A-Za-z0-9_]

            If invalid characters are found, it will replace that
            char with a valid one.

            :param: field_names - a list of str that contains the column names
            :returns: adjusted array that replaces any invalid characters in field names
        """
        adjusted_names = []
        if field_names is not None:
            for name in field_names:
                adj = name
                if name[0].isdigit():
                    adj = name.replace(name[0], digit_converter[name[0]])
                adj = re.sub(r'[\-]', '_', adj)
                adj = re.sub(r'[\W]+', '', adj)
                adjusted_names.append(adj)
        return adjusted_names
                