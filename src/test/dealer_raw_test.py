#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: dealer_raw_test
# author: eva
# date: 2018/1/12
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------


from utils.mysqldb_helper import MysqldbHelper
from utils import general_helper

if __name__ == '__main__':
    mysql = MysqldbHelper()
    # 1. insert
    now_time = general_helper.get_now()
    sql = u"insert into dealer_raw(" \
          u"`main_brand_id`,`main_brand_name`,`main_brand_show`,`brand_name`,`brand_show`,`province_name`,`province_show`," \
          u"`city_name`,`location_name`,`dealer_type`,`dealer_url`,`dealer_name`,`dealer_id`,`dealer_brand`,`dealer_pro_title`," \
          u"`dealer_pro_url`,`dealer_pro_day`,`dealer_add`,`dealer_tel`,`sale_area`,`url`,`create_time`" \
          u") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    params = (
        2, '奥迪', 'audi', '奥迪A6', 'audia6', '北京', 'beijing',
        '北京', '北京', '4S店', 'http://dealer.bitauto.com/10005227', '奥迪腾达店', 10005227, '一汽奥迪', '年终大促',
        'http://dealer.bitauto.com/10005227/news/2000111223', '20', '西直门外大街25号向南100米', '400-880-0134', '京津冀',
        'http://dealer.bitauto.com/10005227', now_time) 
    mysql.insert(sql, params)
    # 2. select

    sql = u"select " \
          u"`main_brand_id`,`main_brand_name`,`main_brand_show`,`brand_name`,`brand_show`,`province_name`,`province_show`," \
          u"`city_name`,`location_name`,`dealer_type`,`dealer_url`,`dealer_name`,`dealer_id`,`dealer_brand`,`dealer_pro_title`," \
          u"`dealer_pro_url`,`dealer_pro_day`,`dealer_add`,`dealer_tel`,`sale_area`,`url`,`create_time` " \
          u" from dealer_raw "
    records = mysql.select(sql)
    print len(records)
