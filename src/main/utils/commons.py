#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: commons
# author: eva
# date: 2018/1/12
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------

import logging.config
import logging
from utils.mysqldb_helper import MysqlHelper
from utils.properties import Properties
import os

file_path = os.path.dirname(__file__)
logging.config.fileConfig(file_path + '/../../config/logger.conf')
logger = logging.getLogger('logger01')

mysql_properties = Properties(file_path + '/../../config/mysql.properties').get_properties()
mysql = MysqlHelper(mysql_properties['host'], user=mysql_properties['user'],
                    password=mysql_properties['password'], db=mysql_properties['db'])
