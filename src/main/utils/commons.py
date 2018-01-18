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
from utils.mysqldb_helper import MysqldbHelper
import os

file_path = os.path.dirname(__file__)
logging.config.fileConfig(file_path + "/../../config/logger.conf")
logger = logging.getLogger("logger01")
mysql = MysqldbHelper()


