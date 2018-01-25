#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: yiche_dealer
# author: eva
# date: 2018/1/8
# version: 0.1.0
# description: crawl data of yiche_dealer, including brand, dealer profile and price.
# ----------------------------------------------------------------------------------------------------------------------

import sys
import re
import multiprocessing
from bs4 import BeautifulSoup
from utils import general_helper

from utils.commons import mysql, logger

project_name = u'易车商家抓取'
main_url = 'http://dealer.bitauto.com'
begin_url = 'http://dealer.bitauto.com/beijing/'
kafka_address = '192.168.171.78:2181,192,168.171.79:2181'
start_url = 'http://dealer.bitauto.com/beijing/'
headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 '
               'Safari/537.36'}


def get_location(soup, div, c):
    """ 获取每个子品牌覆盖的省及直辖市

    :param soup: html in Beautiful soup
    :param div: the div block
    :param c: the content indicator
    :return: location list
    """
    plist = []
    provincelist = soup.find(div, c).find_all('li')
    for province in provincelist:
        p = {}
        p['url'] = re.findall(r'(?<=href=\").*?(?=\">)', str(province))[0]
        p['name'] = re.findall(r'(?<=0\">).*?(?=<)', str(province))[0].decode('utf-8')
        p['show'] = p['url'].split('/')[1]
        p['num'] = re.findall(r'(?<=\().*?(?=\))', str(province))[0]
        plist.append(p)
    return plist


def get_all_province():
    """ 获取区域
    从北京站获取的省和直辖市是全面的，获取每个省和直辖市的名字，每个省和直辖市的品牌是不一样的，
    本来是从每个品牌商家列表上边的区域位置按钮弹层中获得该品牌的覆盖的地区，但是有的品牌不支持这样，
    所以对这些品牌应先获得所有的地区，然后与各品牌拼接url。顺便写入数据库

    以上两种方法结合互补执行

    :return:
    """
    bhtml = general_helper.get_response('http://dealer.bitauto.com/beijing/audi/')
    bsoup = BeautifulSoup(bhtml, 'lxml')
    provincelist = bsoup.find('ul', 'layer-txt-list').find_all('li')
    plist = []
    for province in provincelist:
        p = {}
        p['url'] = re.findall(r'(?<=href=\").*?(?=\">)', str(province))[0].decode('utf-8')
        p['name'] = re.findall(r'(?<=0\">).*?(?=<)', str(province))[0].decode('utf-8')
        p['show'] = p['url'].split('/')[1].decode('utf-8')
        p['num'] = re.findall(r'(?<=\().*?(?=\))', str(province))[0]
        now_time = general_helper.get_now()
        sql = u"insert into province (`name`,`show`,`url`,`create_time`)\
           values ( %s,%s,%s,%s)"
        params = (p['name'], p['show'], p['url'], now_time)
        mysql.insert(sql, params)
        plist.append(p)
    return plist


def get_province(bshow):
    """ 从数据库中读取省直辖市名称与品牌名称构建url，若有经销商则返回该省

    :return:
    """
    sql = u"select distinct `name`, `show` from province"
    relist = mysql.select(sql)
    # closelink(cur,conn)
    plist = []
    for i in range(len(relist)):
        # print relist[i][0]
        para = '/' + relist[i][1] + '/' + bshow + '/?BizModes=0'
        lurl = general_helper.build_url(main_url, para)
        # print lurl
        html = general_helper.get_response(lurl)
        soup = BeautifulSoup(html, 'lxml')
        dealerbox = soup.find('div', 'main-inner-section sm dealer-box')
        dealerlist = dealerbox.find_all('div', 'row dealer-list')
        if len(dealerlist) == 0:
            # print relist[i][0]+'has not dealer'
            continue
        else:
            p = {'name': relist[i][0], 'show': relist[i][1]}
            plist.append(p)
            # print relist[i][0],relist[i][1]+' has dealer'
    return plist


def get_city(p, psoup):  #
    """根据省份信息获取下属城市p={name:,url:,num:,show:}

    :param p:
    :param psoup:
    :return:
    """
    if p['name'] in [u'北京', u'上海', u'天津', u'重庆']:  # 判断是否直辖市,直辖市下面没有城市，所以下属城市是它们自己
        clist = [p]
        # print p['name']
    else:
        clist = get_location(psoup, 'dl', 'f-area')
        # print 'success get city'
    return clist


def get_loc(c, csoup):
    """ 根据城市信息获取下属区县c={name:,url:,num:,show:}

    :param c:
    :param csoup:
    :return:
    """
    if c['name'] in [u'北京', u'上海', u'天津', u'重庆']:  # 直辖市和普通城市下属区县的标签名不一样，故单独处理
        llist = get_location(csoup, 'dl', 'f-area')
    else:
        llist = get_location(csoup, 'div', 'area-sub')

    return llist


def get_dealer_telephone(dealer_id):
    """ 由商家ID获取商家电话，输入商家id为字符串

    :param dealer_id:
    :return:
    """
    url = 'http://autocall.bitauto.com/eil/das2.ashx?userid=' + str(dealer_id) + '&mediaid=10&source=bitauto'
    response = general_helper.get_response(url, False)
    response = response.text
    telstr = re.findall(r'(?<=tel\"\:").*?(?=\")', str(response))
    if not telstr:
        tel = None
    else:
        tel = telstr[0].decode('utf-8')
    return tel


def get_main_brand():
    """ 获取主品牌数据

    :return:
    """
    main_brand_list = []
    # 获取经销商频道左侧品牌导航真正请求的url
    url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jingxiaoshang&pagetype=masterbrand' \
          '&objid=0&citycode=beijing%2F&cityid=201 '
    data = general_helper.get_json_response(url)
    # print data
    main_brand_box = data['brand']
    # print main_brand_box
    for item in main_brand_box.keys():
        main_brand_list0 = main_brand_box[item]
        main_brand_list.extend([{'id': mb['id'], 'name': mb['name'].decode('utf-8'), 'url': mb['url'],
                                 'show': mb['url'].split('/')[2], 'num': mb['num']} for mb in
                                main_brand_list0])
    return main_brand_list


def get_brand(main_brand_list):
    """ 获取子品牌和车型（车型没啥用）
    :param main_brand_list 主品牌列表
    :return: 子品牌列表。[{主品牌：,品牌：,车型{}},{同前},{同前}]列表,元素为每个子品牌的信息，包括所属主品牌信息，子品牌信息，下属车型信息（字典）
    """
    brand_list = []
    for i in range(len(main_brand_list)):
        id = main_brand_list[i]['id']
        main_brand_name = main_brand_list[i]['name']
        main_brand_id = main_brand_list[i]['id']
        main_brand_show = main_brand_list[i]['show']
        main_brand_num = main_brand_list[i]['num']
        main_brand_url = main_brand_list[i]['url']
        url = 'http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?' \
              'tagtype=jingxiaoshang&pagetype=masterbrand&objid=' + str(
            id) + '&citycode=beijing%2F&cityid=201'  # 获取子品牌真正请求的网址
        # print url
        # print main_brand_name
        data = general_helper.get_json_response(url)
        mbrandbox = data['brand']
        # print type(mbrandbox)
        for mbox in mbrandbox.values():
            for mb in mbox:
                if 'child' in mb.keys():
                    # print 'get it'
                    child = mb['child']
                    logger.debug("%s,%s,%s,%s" % (main_brand_name, main_brand_id, main_brand_show, len(child)))
                    for b in child:
                        brand = {'mainbrand': main_brand_name, 'mainid': main_brand_id, 'mainshow': main_brand_show,
                                 'main_url0': main_brand_url, 'mainnum': main_brand_num,
                                 'name': b['name'].decode('utf-8'), 'url': b['url'], 'num': b['num'],
                                 'show': b['url'].split('/')[2]}
                        # print b['url'].split('/')
                        mchild = b['child']  # 品牌下属车型模块
                        brand['model'] = []
                        # print brand['name']#,brand['url'],brand['show']
                        brand_list.append(brand)
                        for m in mchild:
                            model = {}
                            model['name'] = m['name'].decode('utf-8')  # 车型名
                            model['url'] = m['url']  # 车型url
                            # showid=m['url'].split('/')[2].split('-')
                            # id=showid[1]
                            model['show'] = m['url'].split('/')[2]  # 车型缩写
                            model['num'] = m['num']  # 车型经销商数
                            brand['model'].append(model)
                            # print model['name']
                else:
                    continue
    return brand_list


def get_all_dealer(brand_list):
    """ 根据品牌获取品牌覆盖地区再获取商家信息
    :param brand_list
    :return:空。数据存入
    """
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # conn,cur=Linksql('192.168.10.71','datacrowler','1qazXSW@','PriceCrawlerDB')
    conn = None
    cur = None
    for brand in brand_list:  # 每个品牌
        logger.debug('crawling: %s' % brand['name'])
        mbrandname = brand['mainbrand']
        mbrandid = brand['mainid']
        mbrandshow = brand['mainshow']
        bname = brand['name']
        bshow = brand['show']
        if brand['num'] == 0:  # 品牌后数字为0即该品牌没有商家
            continue
        else:
            logger.info("get dealers of %s, %s, %s" % (mbrandname, bname, brand['num'] or 0))
            burl = general_helper.build_url(main_url, brand['url'])
            bhtml = general_helper.get_response(burl)
            bsoup = BeautifulSoup(bhtml, 'lxml')
            try:  # 有的品牌无法从商家列表上边的区域位置按钮弹层中获得该品牌的覆盖的地区，会抛出异常
                plist = get_location(bsoup, 'ul', 'layer-txt-list')
            except Exception, e:
                plist = get_province(main_url, bshow)  # 此时采取第二种方案
                logger.critical("%s, %s, %s" % (bname, len(plist), ' this brand don\'t have dealer'))
                raise
            # brand['location']=[]
            if len(plist) == 0:  # 有的品牌无法从商家列表上边的区域位置按钮弹层中获得该品牌的覆盖的地区，会抛出异常，虽然经过方案二的处理但是有的品牌下没有覆盖省及直辖市，此时plist=[]
                continue
            else:
                for p in plist:
                    pname = p['name']
                    purl = p['url']
                    pshow = p['show']

                    pnum = 0
                    try:
                        pnum = int(p['num'])
                    except Exception, e:
                        logger.critical(e.message)
                        raise
                    finally:
                        pnum = 0

                    purl = general_helper.build_url(main_url, p['url'])
                    location = {'mainbrand': mbrandname, 'mainid': mbrandid, 'mainshow': mbrandshow, 'bname': bname,
                                'bshow': bshow, 'pname': pname, 'pshow': pshow, 'pnum': pnum}
                    # location['purl']=purl
                    if int(p['num']) <= 10:  # 如果全省商家不超过10个就不需要往下找市区县，商家列表10个商家一页，对于超过10个的多页会有重复商家，导致抓取到的商家有漏
                        # print p['name'],' has <10 dealer'
                        get_dealer(purl, location)
                        continue
                    else:
                        phtml = general_helper.get_response(purl)
                        psoup = BeautifulSoup(phtml, 'lxml')
                        # clist=[]

                        clist = get_city(p, psoup)  # 获取省下属市
                        for c in clist:
                            if c['name'] == u'不限':
                                continue
                            else:
                                # print c['name']
                                cname = c['name']
                                curl = c['url']
                                cnum = c['num']
                                cshow = c['show']
                                c_url = general_helper.build_url(main_url, c['url'])
                                if int(cnum) <= 10:  # 如果全市商家不超过10个就不需要往下找区县，商家列表10个商家一页，对于超过10个的多页会有重复商家，导致抓取到的商家有漏
                                    # print c['name'],' has <10 dealers'
                                    get_dealer(c_url, location)
                                    continue
                                else:
                                    chtml = general_helper.get_response(c_url)
                                    csoup = BeautifulSoup(chtml, 'lxml')
                                    try:
                                        llist = get_loc(c, csoup)  # 获取城市下属区县
                                    except Exception, e:
                                        logger.critical("%s, %s, %s" % (brand['name'], p['name'], c['name']))
                                        raise
                                    for l in llist:  # 获取每个商家信息
                                        llurl = general_helper.build_url(main_url, l['url'])
                                        get_dealer(llurl, location)
    return


def get_dealer(lurl, location):
    """从一个品牌区域的url获取商家信息

    :param lurl:
    :param location:
    :return:
    """
    html = general_helper.get_response(lurl)
    # print html.encode('gbk','ignore')
    soup = BeautifulSoup(html, 'lxml')
    # print 'begin get dealer'
    dealerbox = soup.find('div', 'main-inner-section sm dealer-box')
    dealerlist = dealerbox.find_all('div', 'row dealer-list')
    # print dealerlist
    for dealer in dealerlist:
        inf = dealer.find('div', 'col-xs-6 left')
        name = inf.find('h6', 'title-4s').find('a')  # 标题
        dtype = name.find('em').string  # 商家类型
        # print dtype
        durl = re.findall(r'(?<=href=\").*?(?=\")', str(name))[0]  # 商家url
        # print durl
        dname = re.findall(r'(?<=span>).*?(?=<)', str(name))[0].decode('utf-8')  # 商家名称
        # print dname
        dealer_id = int(re.findall(r'(?<=com/)\d+(?=/)', str(durl))[0])  # 商家ID
        # print dealer_id

        dpinpai = re.findall(r'(?<=span\>).*?(?=\<)', str(inf.find('p', 'brand')))[0].decode('utf-8')  # 商家主营品牌
        # print dpinpai
        if inf.find('p', 'promote') != None:  # 判断商家是否有正在进行的降价
            dpromotetitle = inf.find('p', 'promote').find('a').string.decode('utf-8').replace(r'\s+', u' ')
            dpromoteurl = re.findall(r'(?<=href=\").*?(?=\")', str(inf.find('p', 'promote').find('a')))[0].decode(
                'utf-8')
            dpromoteday = inf.find('p', 'promote').find('span', 'time').string.decode('utf-8')
        else:
            dpromotetitle = None  # 商家正在进行的降价标题
            dpromoteurl = None  # 降价新闻的url
            dpromoteday = None  # 剩余天数
        # print dpromotetitle
        # print dpromoteurl
        # print dpromoteday
        add = inf.find('p', 'add').find_all('span', attrs={'title': True})[0].attrs['title'].replace(u'\xa0',
                                                                                                     u'')  # 商家地址
        # print add.encode('gbk','ignore')
        tel = get_dealer_telephone(dealer_id)
        dtel = tel  # 商家电话
        # print dtel.encode('gbk','ignore')
        try:
            dsalearea = inf.find('p', 'tel').find('span', 'sales-area').string  # 售卖地区
        except Exception, e:
            print lurl, dname, location['pname'], location['mainbrand'], location['bname'], inf.find('p', 'tel')
            raise
        dcity = dealer.find('div', 'col-xs-7 middle').p.string.split(' ')[0]  # 所在城市
        dlocation = dealer.find('div', 'col-xs-7 middle').p.string.split(' ')[1].replace('&nbsp;', '')  # 所在地区
        now_time = general_helper.get_now()
        logger.debug("%s,%s,%s,%s,%s" % (location['pname'], dcity, dlocation, dealer_id, dname))
        sql = u"insert into dealer_raw(" \
              u"`main_brand_id`,`main_brand_name`,`main_brand_show`,`brand_name`,`brand_show`,`province_name`,`province_show`," \
              u"`city_name`,`location_name`,`dealer_type`,`dealer_url`,`dealer_name`,`dealer_id`,`dealer_brand`,`dealer_pro_title`," \
              u"`dealer_pro_url`,`dealer_pro_day`,`dealer_add`,`dealer_tel`,`sale_area`,`url`,`create_time`" \
              u") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
            location['mainid'], location['mainbrand'], location['mainshow'], location['bname'], location['bshow'],
            location['pname'], location['pshow'], dcity, dlocation, dtype, durl.decode('utf-8'), dname, dealer_id,
            dpinpai,
            dpromotetitle or '', dpromoteurl or '', dpromoteday or '', add, dtel or '', dsalearea,
            lurl.decode('utf-8'),
            now_time)
        # print sql
        try:
            mysql.insert(sql, params)
        except Exception, e:
            print 'this is an except:', str(e)
            print sql
            print location['mainid'], location['mainbrand'], location['mainshow'], location['bname'], location[
                'bshow'], location['pname'], location['pshow']
            print dcity, dlocation
            print dtype, durl, dname, dealer_id
            print dpinpai
            print dpromotetitle, dpromoteurl, dpromoteday
            print add.encode('gbk', 'ignore'), dtel, dsalearea
            print lurl
            raise
            # raw_input('raw_input:')

    # print 'get one page'
    # time.sleep(10)
    nexton = soup.find('a', 'next_on')
    # print nexton
    if nexton is None:  # 判断是否有下一页
        # print 'get one location'
        return
    else:
        # print nexton
        # time.sleep(10)
        nurl = re.findall(r'(?<=href=\").*?(?=\")', str(nexton).replace('amp;', ''))[0]
        nexturl = general_helper.build_url(main_url, nurl)
        # print nexturl
        # time.sleep(10)
        get_dealer(nexturl, location)
        return


def crawl():
    # 获取所有省份
    logger.info("start: get all provinces.")
    get_all_province()
    logger.info("finish: get all provinces.")

    # 获取主品牌和品牌
    logger.info("start: get main brands.")
    main_brand_list = get_main_brand()
    logger.info("finish: get main brands.")

    logger.info("start: get brands.")
    brand_list = get_brand(main_brand_list)
    logger.info("finish: get brands.")

    success = 0
    start_time = general_helper.get_now()
    # print start_time
    sql = u"insert into crawl_log (project_name,complete_success,start_time)  values (%s, %s, %s)"
    params = (u'易车商家抓取', success, start_time)
    mysql.insert(sql, params)

    # get_all_dealer(brand_list[0:1])
    l = len(brand_list)
    a = l / 4
    b = (l / 4) * 2
    c = (l / 4) * 3
    print a, b, c
    brand_list1 = brand_list[0:a]
    brand_list2 = brand_list[a:b]
    brand_list3 = brand_list[b:c]
    brand_list4 = brand_list[c:]
    print len(brand_list1), len(brand_list2), len(brand_list3), len(brand_list4)

    p1 = multiprocessing.Process(target=get_all_dealer, args=(brand_list1,))
    p2 = multiprocessing.Process(target=get_all_dealer, args=(brand_list2,))
    p3 = multiprocessing.Process(target=get_all_dealer, args=(brand_list3,))
    p4 = multiprocessing.Process(target=get_all_dealer, args=(brand_list4,))
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
    sql = u"update crawl_log set complete_success = %s, end_time = %s where id = (" \
          u"select id from ( " \
          u"select max(id) as id from crawl_log as a where project_name= %s ) as s)"
    params = (success, end_time, project_name)
    mysql.update(sql, params)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    crawl()
