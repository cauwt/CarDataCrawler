#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: mysqldb_helper_test
# author: eva
# date: 2018/1/12
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------

from utils import general_helper
from utils.commons import mysql

if __name__ == '__main__':
    # 1. insert
    success = 0
    start_time = general_helper.get_now()
    # print start_time
    sql = u"insert into crawl_log (project_name,complete_success,start_time)  VALUES (%s, %s, %s)"
    params = (u'易车商家抓取', success, start_time)
    mysql.insert(sql, params)

    success = 1
    end_time = general_helper.get_now()
    sql = u"update crawl_log set complete_success = %s, end_time = %s where id = (" \
          u"select id from ( " \
          u"select max(id) as id from crawl_log as a where project_name='易车商家抓取') as s)"
    params = (success, end_time)
    mysql.update(sql, params)

pass



