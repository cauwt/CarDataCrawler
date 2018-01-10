#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: general
# author: eva
# date: 2018/1/8
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------
import json
import re
import time


def get_now_date():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def get_json(content):
    try:
        response = json.loads(content)
    except Exception, e:
        # 返回的json不规范抛出异常
        # print 'this is an except:',str(e)
        content1 = re.sub(r"(,|\{)(\w+?)\s*?:", r'\1"\2":', response)
        response = eval(content1)
    return response


def build_url(main_url, param):
    url = main_url + param
    return url
