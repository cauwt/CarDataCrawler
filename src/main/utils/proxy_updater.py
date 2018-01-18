#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: proxy_updater
# author: eva
# date: 2018/1/17
# version: 
# description:定期更新代理。从xicidaili中获取代理，并保存其中的可用代理
# ----------------------------------------------------------------------------------------------------------------------


import urllib2
import re
import time
import urllib
import socket
socket.setdefaulttimeout(3)



def verify_ip(ip_port):
    verify_url = 'http://ip.chinaz.com/getip.aspx'
    proxy = {'http': 'http://' + ip_port}
    try:
        urllib.urlopen(verify_url, proxies=proxy).read()
        return True
    except Exception, e:
        return False


if __name__ == '__main__':
    main_url = 'http://www.xicidaili.com/nn'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Hosts': 'hm.baidu.com',
        'Referer': main_url,
        'Connection': 'keep-alive'
    }

    proxy_file = '../../config/proxy.txt'

    f = open(proxy_file, "w")
    total = 0
    yes = 0
    # 指定爬取范围（这里是第1~1000页）
    for i in range(1, 100):
        url = main_url + '/' + str(i)
        print "crawling: %s " % url
        req = urllib2.Request(url=url, headers=headers)
        res = urllib2.urlopen(req).read()

        # 提取ip和端口
        ip_list = re.findall("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})", res, re.S)

        # 将提取的ip和端口写入文件
        for li in ip_list:
            ip_port = li[0] + ':' + li[1]
            line = ip_port + '\n'
            total += 1
            if verify_ip(ip_port):
                yes +=1
                print ip_port + ' yes'
                f.write(line)
            else:
                print ip_port + ' no'
        f.flush()
        time.sleep(2)  # 每爬取一页暂停两秒
    f.close()
    print 'total= %d, yes = %d, no = %d' % (total,yes, total - yes)
