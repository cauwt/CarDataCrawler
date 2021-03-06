#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: general_helper
# author: eva
# date: 2018/1/8
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------

import json
import re
import time
import urllib2
import logging

import requests

import commons

import random
import os


logger = logging.getLogger("logger01")
file_path = os.path.dirname(__file__)
user_agent_list = []
f = open(file_path + '/../../config/user_agent.txt', 'r')
for line in f:
    user_agent_list.append(line.replace('\r\n', ''))
f.close()

proxy_list = []
f = open(file_path + '/../../config/proxy.txt', 'r')
for line in f:
    proxy_list.append(line.replace('\n', ''))
f.close()


def get_now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def str_to_time(string):
    timestr = re.findall(r'\d+', string)
    times = '-'.join(timestr).decode('utf-8')
    return times


def get_json_response(url):
    """ 获取响应结果中的json内容
    起初的响应结果形式如下:JsonCallBack({id:...})，
    需要做两步处理：1.只要小括号内的json串，2.将key的名称使用双引号引起来，以符合json的形式
    :param url:
    :return:
    """
    user_agent = random.choice(user_agent_list).strip("\r\n ")
    request = urllib2.Request(url)
    request.add_header('User-Agent',
                       user_agent)

    # proxy = random.choice(proxy_list).strip("\r\n ")
    # request.set_proxy(proxy, 'http')

    retries = 3
    while retries > 0:
        try:
            response = urllib2.urlopen(request, timeout=30).read().decode('utf-8', 'ignore')
            content = re.findall(r'(?<=\().*(?=\))', response)[0]
            break

        except Exception, e:
            retries -= 1
            logger.debug("%s times to retry" % format(str(retries)))
            time.sleep(5)
    if retries == 0:
        raise
    try:
        response = json.loads(content)
    except Exception, e:
        # 返回的json不规范抛出异常
        # print 'this is an except:',str(e)
        content1 = re.sub(r'([,{])\s*(\w+?)\s*?:', r'\1"\2":', content)
        response = eval(content1)
    return response


def get_response(url, keep_alive=True):
    """ 请求页面获取html

    :param url:
    :return:
    """
    response = None
    user_agent = random.choice(user_agent_list).strip("\r\n ")
    request = urllib2.Request(url)
    request.add_header('User-Agent', user_agent)

    # proxy = random.choice(proxy_list).strip("\r\n ")
    # request.set_proxy(proxy, 'http')

    retries = 3
    while retries > 0:
        try:
            if keep_alive:
                response = urllib2.urlopen(request, timeout=30).read().decode('utf-8', 'ignore')
            else:
                s = requests.session()
                s.keep_alive = False  # requests默认保持连接，打开太多又不关闭会报错，故将保持连接关掉
                response = s.get(url, timeout=30)
            break
        except Exception, e:
            retries -= 1
            logger.debug("%s times left to retry" % format(str(retries)))
            time.sleep(5)
    if retries == 0:
        raise
    return response


def build_url(main_url, param):
    url = main_url + param
    return url
