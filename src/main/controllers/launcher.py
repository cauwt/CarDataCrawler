#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: launcher
# author: eva
# date: 2018/1/8
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------
import sys

from spiders.yiche_dealer import YicheDealer

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")

    yiche_spider = YicheDealer()
    yiche_spider.get_main_brand()
