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

logging.config.fileConfig("../../config/logger.conf")
logger = logging.getLogger("logger01")
mysql = MysqldbHelper()


