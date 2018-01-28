#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: yiche_car
# author: eva
# date: 2018/1/26
# version: 
# description: 抓取车型数据，使用lxml.xpath解析
# ----------------------------------------------------------------------------------------------------------------------


import sys
import re
from lxml import etree
from utils import general_helper
from utils.commons import mysql
from utils.commons import logger


def get_main_brand():
    """获取主品牌信息
    可以得到以下信息：
    main_brand_id
    main_brand_name

    :return: 主品牌列表
    """
    main_brand_list = []
    main_brand_url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=0'
    data = general_helper.get_json_response(main_brand_url)
    main_brand_dict = data['brand']
    for key in main_brand_dict:
        main_brand_list0 = main_brand_dict[key]
        main_brand_list.extend([{'main_brand_id': mb['id'], 'main_brand_name': mb['name'].decode('utf-8')} for mb in
                                main_brand_list0])
    return main_brand_list


def get_brand_serial(main_brand_list):
    """根据主品牌ID获取品牌与车型信息
    可以得到以下信息：
    brand_id
    brand_name,
    serial_id
    serial_name

    :param main_brand_list:
    :return:品牌车型列表
    """
    brand_serial_list = []
    brand_serial_url_base = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=@main_brand_id'
    for main_brand_item in main_brand_list:
        brand_serial_url = brand_serial_url_base.replace('@main_brand_id', str(main_brand_item['main_brand_id']))
        data = general_helper.get_json_response(brand_serial_url)
        main_brand_box = data['brand']
        for key1 in main_brand_box:
            for mb in main_brand_box[key1]:
                if 'child' in mb:
                    logger.debug(main_brand_item['main_brand_name'])
                    for brand_item in mb['child'] or []:
                        brand = {'main_brand_id': main_brand_item['main_brand_id'],
                                 'main_brand_name': main_brand_item['main_brand_name'],
                                 'brand_id': int(re.search(r'\d+', str(brand_item['url'])).group()),
                                 'brand_name': brand_item['name'].decode('utf-8'),
                                 'serial': []}
                        if 'child' in brand_item:
                            for serial_item in brand_item['child'] or []:
                                serial = {'serial_id': int(re.search(r'\d+', str(serial_item['url'])).group()),
                                          'serial_name': serial_item['name'].decode('utf-8')}
                                brand['serial'].append(serial)
                            brand_serial_list.append(brand)
                        else:
                            continue
                else:
                    continue
    return brand_serial_list
    pass


def insert_car_to_db(brand_serial_car_list):
    """ 将车款数据插入数据库

    :param brand_serial_car_list:
    :return:
    """
    sql = 'INSERT INTO car_data.car ( main_brand_id, main_brand_name, brand_id, brand_name, ' \
          'serial_id, serial_name, serial_spell, serial_show_name, car_id, car_name, car_gear, ' \
          'car_engine_displacement, car_msrp, car_sale_year, create_time) ' \
          'VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    now = general_helper.get_now()
    params_list = []

    for car in brand_serial_car_list:
        params = (car['main_brand_id'], car['main_brand_name'], car['brand_id'], car['brand_name'],
                  car['serial_id'], car['serial_name'], car['serial_spell'], car['serial_show_name'],
                  car['car_id'], car['car_name'], car['car_gear'], car['car_engine_displacement'],
                  car['car_msrp'] or 0.0, car['car_sale_year'], now)
        params_list.append(params)

    mysql.insert_batch(sql, params_list)

    pass


def get_and_insert_car(brand_serial_list):
    """根据车型ID获取车款信息，以及补充车型信息
    可以得到以下信息
    serial_spell,
    serial_show_name,

    car_id,
    car_name,
    car_gear,
    car_engine_displacement,
    car_msrp,
    car_sale_year

    :param brand_serial_list:
    :return:主品牌品牌车型车款列表
    """
    serial_url_base = 'http://car.bitauto.com/tree_chexing/sb_@serial_id'
    for brand in brand_serial_list:
        logger.debug('brand: %s' % (brand['brand_name']))
        brand_serial_car_list = []
        for serial in brand['serial']:
            logger.debug('serial: %s' % (serial['serial_name']))
            serial_id = serial['serial_id']
            serial_url = serial_url_base.replace('@serial_id', str(serial_id))
            logger.debug('url: %s' % serial_url)
            content = general_helper.get_response(serial_url)
            html = etree.HTML(content)
            serial_spell = str(html.xpath('//div[@class="section-header header1"]/div/h2/a/@href')[0])[1:-1]
            serial_show_name = str(html.xpath('//div[@class="section-header header1"]/div/h2/a/text()')[0]).decode('utf-8')
            car_row_list = html.xpath('//table[@id="compare_sale"]/tbody/tr')
            for car_row in car_row_list:
                if 'class' in car_row.attrib and car_row.attrib['class'] == 'table-tit':  # 分组表头
                    car_engine_displacement = str(car_row.xpath('string(th[@class="first-item"])')).decode('utf-8')
                else:  # 车款
                    car_id = int(re.search(r'\d+', car_row.attrib['id']).group().strip())
                    car_name = str(car_row.xpath('td/a/text()')[0]).strip().decode('utf-8')
                    car_gear = str(car_row.xpath('string(td[3])')).strip().decode('utf-8')
                    car_msrp_match = re.search(r'(\d+(\.\d+)?)', str(car_row.xpath('string(td[@class="txt-right"]/span)')).strip())
                    car_msrp = car_msrp_match.group() if car_msrp_match else 0.0

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
                                        'car_engine_displacement': car_engine_displacement,
                                        'car_msrp': car_msrp,
                                        'car_sale_year': car_sale_year
                                        }
                    brand_serial_car_list.append(brand_serial_car)
        insert_car_to_db(brand_serial_car_list)


def crawl():
    logger.debug("getting main brand list")
    main_brand_list = get_main_brand()
    logger.debug('getting brand serial list')
    brand_serial_list = get_brand_serial(main_brand_list)
    logger.debug('getting and inserting car list')
    get_and_insert_car(brand_serial_list)
    pass


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    crawl()
