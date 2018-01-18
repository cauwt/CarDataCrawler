#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: promotion_price_test
# author: eva
# date: 2018/1/17
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------


from utils.mysqldb_helper import MysqldbHelper
from utils import general_helper

if __name__ == '__main__':
    mysql = MysqldbHelper()
    # 1. insert
    now_time = general_helper.get_now()
    sql = u"insert into car_data.promotion_price (dealer_id, dealer_name, model_id, model_name, model_down_url, title, " \
          u"publish_date, begin_date, end_date, style_id, style_name, style_msrp, style_promo, style_price, " \
          u"style_store, create_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    params = (
        10005227, u'奥迪腾达店', 2353, u'奥迪A6', 'http://dealer.bitauto.com/10005227/audia6', u'年终大促',
        '2018-01-12', '2018-01-12', '2018-02-10', 130256, u'2018款 奥迪A6 2018 标准版', '23.25', '22.25', '23.25',
        u'库存充足', now_time)
    mysql.insert(sql, params)
    # 2. select

    sql = u"select " \
          u"dealer_id, dealer_name, model_id, model_name, model_down_url, title," \
          u"publish_date, begin_date, end_date, style_id, style_name, style_msrp, style_promo, style_price," \
          u"style_store, create_time " \
          u" from car_data.promotion_price "
    records = mysql.select(sql)
    print len(records)
