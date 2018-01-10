#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: logging_test
# author: eva
# date: 2018/1/10
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------


import logging
import logging.config

if __name__ == '__main__':
    main_brand_list = [1, 2, 3, 4]
    logging.config.fileConfig("../config/logger.conf")
    logger = logging.getLogger("example01")

    logger.debug('This is debug message')
    logger.info('This is info message')
    logger.warning('This is warning message')
    #
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='[%(asctime)s] %(levelname)s: %(message)s ',
    #                     datefmt='%H:%M:%S')
    #
    # print "length of main_brand_list: %s " % len(main_brand_list)
    #
    # logging.debug('This is debug message')
    # logging.info('This is info message')
    # logging.warning('This is warning message')
    # logging.error('This is error message')
    # logging.critical('This is critical message')
    #
    # logging.info("length of main_brand_list: %s ", len(main_brand_list))
