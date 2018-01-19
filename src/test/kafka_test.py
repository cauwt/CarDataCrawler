#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: kafka_test
# author: eva
# date: 2018/1/18
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------

from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json

from utils import general_helper


def main():
    topic = 'yiche_promotion_price'
    zookeeper_list = '192.168.171.78:9092,192.168.171.79:9092'
    # 1. send price data in json

    # price = {
    #     'dealer_id': 10005227,
    #     'dealer_name': '奥迪腾达店',
    #     'model_id': 2353,
    #     'model_name': '奥迪A6',
    #     'model_down_url': 'http://dealer.bitauto.com/10005227/audia6',
    #     'title': '年终大促',
    #     'publish_date': '2018-01-12',
    #     'begin_date': '2018-01-12',
    #     'end_date': '2018-02-10',
    #     'style_id': 130256,
    #     'style_name': '2018款 奥迪A6 2018 标准版',
    #     'style_msrp': '23.25',
    #     'style_promo': '22.25',
    #     'style_price': '23.25',
    #     'style_store': '库存充足',
    #     'create_time': str(general_helper.get_now())
    # }
    # data = json.dumps(price)
    # producer = KafkaProducer(bootstrap_servers=zookeeper_list)
    # producer.send(topic, data)
    # producer.flush()

    # 2. receive the message
    group_id = 'price_hdfs'
    consumer = KafkaConsumer(topic, group_id=group_id,
                             bootstrap_servers=zookeeper_list)

    try:
        for message in consumer:
            print message
    except KeyboardInterrupt, e:
        print e

    pass


if __name__ == '__main__':
    main()
    pass
