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

logger = logging.getLogger("logger01")


def get_now_date():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def get_json_response(url):
    """ 获取响应结果中的json内容
    起初的响应结果形式如下:JsonCallBack({id:...})，
    需要做两步处理：1.只要小括号内的json串，2.将key的名称使用双引号引起来，以符合json的形式
    :param url:
    :return:
    """
    response = None
    request = urllib2.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
    retries = 3
    while (retries > 0):
        try:
            response = urllib2.urlopen(request, timeout=30).read().decode('utf-8', 'ignore')
            content = re.findall(r'(?<=\().*(?=\))', response)[0]
            break

        except Exception, e:
            retries -= 1
            logger.debug("%s times to retry" % format(str(retries)))
            time.sleep(5)
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
    request = urllib2.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
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

    return response


def build_url(main_url, param):
    url = main_url + param
    return url
