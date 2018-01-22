#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: province_test
# author: eva
# date: 2018/1/12
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------

from utils import general_helper
from utils.commons import mysql


if __name__ == '__main__':
    # 1. insert
    now_time = general_helper.get_now()
    sql = u"insert into province (`name`,`show`,`url`,`create_time`)\
               values ( %s,%s,%s, %s)"
    params = ('北京', 'beijing', 'http://beijing.bitauto.com', now_time)
    mysql.insert(sql, params)

    # 2. select
    sql = u"select distinct `name`,`show` from province"
    params = ('北京', 'beijing', 'http://beijing.bitauto.com', now_time)
    records = mysql.select(sql)
    print len(records)

pass



