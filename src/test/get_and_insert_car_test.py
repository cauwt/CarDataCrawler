#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: get_car_list
# author: eva
# date: 2018/1/26
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------

import sys
from bs4 import BeautifulSoup
import re
from lxml import etree

from spiders.yiche_car import insert_car_to_db
from utils import general_helper

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    serial_url = 'http://car.bitauto.com/tree_chexing/sb_1608'
    content = general_helper.get_response(serial_url)
    html = etree.HTML(content)
    serial_spell = str(html.xpath('//div[@class="section-header header1"]/div/h2/a/@href')[0])[1:-1]
    serial_show_name = str(html.xpath('//div[@class="section-header header1"]/div/h2/a/text()')[0]).decode('utf-8')
    car_row_list = html.xpath('//table[@id="compare_sale"]/tbody/tr')
    brand_serial_car_list = []
    for car_row in car_row_list:
        if 'class' in car_row.attrib and car_row.attrib['class'] == 'table-tit':  # 分组表头
            car_engine = str(car_row.xpath('normalize-space(th[@class="first-item"])')).decode('utf-8')
        else:  # 车款
            car_id = int(re.search(r'\d+', car_row.attrib['id']).group())
            car_name = str(car_row.xpath('td/a/text()')[0]).strip().decode('utf-8')
            car_gear = str(car_row.xpath('string(td[3])')).strip().decode('utf-8')
            car_msrp_temp = re.search(r'(\d+(\.\d+)?)', str(car_row.xpath('string(td[@class="txt-right"]/span)')).strip())
            car_msrp = car_msrp_temp.group() if car_msrp_temp else 0.0

            car_sale_year = re.search(r'^\d+', car_name).group() or ''
            brand_serial_car = {'main_brand_id': 3,
                                'main_brand_name': u'宝马',
                                'brand_id': 20005,
                                'brand_name': u'进口宝马',
                                'serial_id': 3486,
                                'serial_name': u'4系',
                                'serial_spell': serial_spell,
                                'serial_show_name': serial_show_name,
                                'car_id': car_id,
                                'car_name': car_name,
                                'car_gear': car_gear,
                                'car_engine': car_engine,
                                'car_msrp': car_msrp,
                                'car_sale_year': car_sale_year
                                }
            brand_serial_car_list.append(brand_serial_car)
    insert_car_to_db(brand_serial_car_list)
