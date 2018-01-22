#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: kafka_util
# author: eva
# date: 2018/1/19
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------


from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json


class KafkaUtilProducer(object):
    """使用kafka的生产模块

    """

    def __init__(self, bootstrap_servers, kafka_topic):
        self.bootstrap_servers = bootstrap_servers
        self.kafka_topic = kafka_topic
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send_json_data(self, params):
        try:
            params_message = json.dumps(params)
            producer = self.producer
            producer.send(self.kafka_topic, params_message.encode('utf-8'))
            producer.flush()
        except KafkaError as e:
            print e


class KafkaUtilConsumer():
    """使用Kafka—python的消费模块

    """

    def __init__(self, bootstrap_servers, kafka_topic, group_id):
        self.bootstrap_servers = bootstrap_servers
        self.kafka_topic = kafka_topic
        self.group_id = group_id
        self.consumer = KafkaConsumer(self.kafka_topic, group_id=self.group_id,
                                      bootstrap_servers=self.bootstrap_servers)

    def consume_data(self):
        try:
            for message in self.consumer:
                # print json.loads(message.value)
                yield message
        except KeyboardInterrupt, e:
            print e
