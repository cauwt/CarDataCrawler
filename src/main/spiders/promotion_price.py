#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: promo_price
# author: eva
# date: 2018/1/17
# version: 
# description: 抓取降价信息
# ----------------------------------------------------------------------------------------------------------------------


import sys
from bs4 import BeautifulSoup
import re
import time
import multiprocessing

from utils.commons import mysql
from utils import general_helper


def get_dealer_from_db():
    """从数据库中读取商家

    :return:
    """
    sql = u"select distinct dealer_id,dealer_name,dealer_url from car_data.dealer_raw "  # \
    #      u"where cast(create_time as date)=cast(now() as date)"
    dealer_list = mysql.select(sql)
    return dealer_list


def get_all_promotion_price(dealer_list, main_url):
    """获取所有降价

    :param dealer_list:
    :param main_url:
    :return:
    """
    for dealer in dealer_list:
        dealer_id = dealer['dealer_id']
        dealer_name = dealer['dealer_name']
        dealer_url = dealer['dealer_url']
        durl = re.sub(r'\?.+', 'cars.html', dealer_url)  # 从商家url修改为商家报价页url
        # print durl
        print dealer_name
        modeldown = get_promotion_price(durl, main_url)  # 获取每个商家的车型降价列表[{name:,},{}]

        if modeldown == []:  # 判断商家是否有降价列表
            # print 'this dealer dont have modeldown'
            continue
        else:
            for model in modeldown:
                modelid = model['id']
                modelname = model['name']
                modeldownurl = model['downurl']
                jiangjia = model['jiangjia']  # 车型降价列表
                # print type(jiangjia)
                for style in jiangjia:  # 每个车型的降价新闻
                    # print style
                    title = style['title']
                    publishdate = style['publishdate']
                    begintime = style['begintime']
                    endtime = style['endtime']
                    styleid = style['styleID']
                    stylename = style['stylename']
                    msrp = style['stylemsrp']
                    jiangjia = style['jiangjia']
                    youhui = style['youhui']
                    kuxun = style['kucun']
                    nowtime = general_helper.get_now()
                    sql = u"insert into car_data.promotion_price (dealer_id, dealer_name, model_id, model_name, model_down_url, title, " \
                          u"publish_date, begin_date, end_date, style_id, style_name, style_msrp, style_promo, style_price, " \
                          u"style_store, create_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    params = (
                        dealer_id, dealer_name, modelid, modelname, modeldownurl, title,
                        publishdate, begintime, endtime, styleid, stylename, msrp, jiangjia or '', youhui,
                        kuxun, nowtime)
                    try:
                        mysql.insert(sql, params)  # 插入数据
                    except Exception, e:
                        print 'this is an except:', str(e)
                        print dealer_id, dealer_name, modelid, modelname, modeldownurl, title, publishdate, begintime, endtime, styleid, stylename, msrp, jiangjia, youhui, kuxun, durl
                        raise
    return


def get_promotion_price(durl, main_url):
    """从商家车型报价页获取降价车型
    
    :param durl: 
    :param main_url: 
    :return: 
    """
    reload(sys)
    sys.setdefaultencoding("utf-8")

    html = general_helper.get_response(durl)
    # print html.decode('utf-8','ignore').encode('gbk','ignore')
    soup = BeautifulSoup(html, 'lxml')
    jiangjiasoup = soup.find('div', 'markdowns')
    modeldown = []
    if jiangjiasoup is not None:  # 有的商家车型降价新闻url无效
        print 'this dealer has jiangjia'
        downbox = jiangjiasoup.find_all('tr')
        for tr in downbox:
            if tr.find_all('td') != []:  # 有的商家降价新闻中并没有车款降价
                model = {}
                a = tr.find('td', 't_l').find('a')
                model['name'] = a.string.decode('utf-8')  # 车型名
                print model['name']
                model['downurl'] = re.findall(r'(?<=href=\").*?(?=\")', str(a))[0]
                print model['downurl']
                downurl = general_helper.build_url(main_url, model['downurl'])
                model['id'] = re.findall(r'\d+(?=\.html)', model['downurl'])[0]  # 车型ID
                # print downurl
                tablelist = get_promotion_price_by_model(downurl)
                if tablelist != None:
                    model['jiangjia'] = tablelist
                    modeldown.append(model)
                else:
                    continue
            else:
                continue
    else:
        print 'this dealer has no promotion price'
        print durl
    return modeldown


def get_promotion_price_by_model(download_url):
    """根据每一个车型获取降价车款

    :param download_url:
    :return:
    """
    html = general_helper.get_response(download_url)
    # print html.decode('utf-8','ignore').encode('gbk','ignore')

    soup = BeautifulSoup(html, 'lxml')
    maincon = soup.find('div', 'con_main art_main')  # 新闻内容
    # print 'maincon:',maincon
    if maincon == None:  # 有的车型降价新闻url无效不能进入降价新闻页会直接跳到新闻列表页，可通过判断页面是否有新闻内容标签判断
        print 'this model is invalid'
        return None
    else:
        titlestr = maincon.find('h1', 'ad').string
        title = re.findall(r'\S+', str(titlestr))[0].decode('utf-8')  # 标题
        publishstr = maincon.find('div', 'subinfo').find('span', 'fl')
        publishdates = re.findall(r'(?<=：)\S+(?=\<)', str(publishstr))[0].decode('utf-8')
        publishdate = general_helper.str_to_time(publishdates)  # 发布日期
        # print publishdate
        saletimestr = maincon.find('div', 'saletime')
        salebegintime = re.findall(r'(?<=：)\S+(?=\s\-)', str(saletimestr))[0].decode('utf-8')
        saleendtime = re.findall(r'(?<=\-\s)\S+(?=，)', str(saletimestr))[0].decode('utf-8')
        # print salebegintime,saleendtime
        # time.sleep(10)
        begintime = general_helper.str_to_time(str(salebegintime))  # 开始时间
        endtime = general_helper.str_to_time(str(saleendtime))  # 结束时间
        # print begintime,endtime
        # print remaimtime
        if soup.find('div', 'art_table') == None:  # 有的降价新闻里并没有降价车款
            return None
        else:
            table = soup.find('div', 'art_table').find_all('tr')  # 降价表第一行为字段名
            # print table
            table_list = []

            for row in table:
                # print row
                elements = row.find_all('td')
                # print elements
                if len(elements) > 1:  # 判断是否是降价变的字段名行
                    style_dict = {}
                    style = row.find('td', 't_l')
                    # print style
                    # print style.find('a')

                    try:
                        styleID = re.findall(r'(?<=_)\d+(?=\.html)', str(style.find('a')))[0]  # 车款ID
                        stylenamelist = re.findall(r'(\S+)', str(style.find('a').string))  # 车款名字
                        stylename = ' '.join(stylenamelist).decode('utf-8')
                    except Exception, e:  # 有的车款没有报价页链接，无法从其链接中找到车款id
                        styleID = 0
                        stylename = style.find('span').string
                    # print styleID


                    # print stylename

                    msrpstr = row.find_all('td', attrs={'class': False})[0].string
                    # print msrpstr
                    msrp = re.findall(r'\S+', str(msrpstr))[0].decode('utf-8')  # 车款msrp
                    print msrp

                    try:  # 有的降价新闻中虽然有降价车款表但是这些车款没有优惠
                        jaj = re.findall(r'\S+', str(row.find('span', 'jade').string))
                        jiangjia = ''.join(jaj).replace('↓', '').decode('utf-8')  # 车款优惠金额
                        kucunstr = row.find_all('td', attrs={'valign': 'middle'})[1]
                    except Exception, e:  # 没有优惠就抛出异常，另起优惠为none
                        jiangjia = None
                        kucunstr = row.find_all('td', attrs={'valign': 'middle'})[0]
                    # print jiangjia

                    youhui = re.findall(r'\S+', str(row.find('td', 'imp').string))[0].decode('utf-8')  # 车款优惠后金额
                    # print youhui


                    # print kucunstr

                    kucun = re.findall(r'\S+', str(kucunstr))[2].decode('utf-8')  # 车款库存
                    # print kucun

                    # print styleID,stylename,msrp,jiangjia,youhui,kucun
                    style_dict['title'] = title
                    style_dict['publishdate'] = publishdate
                    style_dict['begintime'] = begintime
                    style_dict['endtime'] = endtime
                    style_dict['styleID'] = styleID
                    style_dict['stylename'] = stylename
                    style_dict['stylemsrp'] = msrp
                    style_dict['jiangjia'] = jiangjia
                    style_dict['youhui'] = youhui
                    style_dict['kucun'] = kucun
                    table_list.append(style_dict)

                else:
                    continue
            return table_list


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    main_url0 = 'http://dealer.bitauto.com'
    project_name = u'易车降价抓取'
    start_time = general_helper.get_now()
    # print start_time
    success = 0
    fsql = u"insert into car_data.crawl_log (project_name,complete_success,start_time) " \
           u"values (%s, %s, %s)"
    params = (project_name, success, start_time)
    mysql.insert(fsql, params)
    relist = get_dealer_from_db()
    print 'success get dealer', len(relist)

    # relist1 = relist[0:10]
    # get_all_promotion_price(relist1, main_url0)
    l = len(relist)
    a = l / 4
    b = (l / 4) * 2
    c = (l / 4) * 3
    print a, b, c
    relist1 = relist[0:a]
    relist2 = relist[a:b]
    relist3 = relist[b:c]
    relist4 = relist[c:]
    print len(relist1), len(relist2), len(relist3), len(relist4)

    p1 = multiprocessing.Process(target=get_all_promotion_price, args=(relist1, main_url0))
    p2 = multiprocessing.Process(target=get_all_promotion_price, args=(relist2, main_url0))
    p3 = multiprocessing.Process(target=get_all_promotion_price, args=(relist3, main_url0))
    p4 = multiprocessing.Process(target=get_all_promotion_price, args=(relist4, main_url0))
    p1.start()  # 启动进程
    p2.start()
    p3.start()
    p4.start()
    p1.join()  # 等子进程结束才执行主进程
    p2.join()
    p3.join()
    p4.join()

    success = 1
    end_time = general_helper.get_now()
    sql = u"update car_data.crawl_log set complete_success = %s, end_time = %s where id = (" \
          u"select id from ( " \
          u"select max(id) as id from crawl_log as a where project_name= %s ) as s)"
    params = (success, end_time, project_name)
    mysql.update_by_param(sql, params)
