# -*- coding:utf-8 -*-
import scrapy
import re

from utils.mysqldb_helper import MysqldbHelper

from yichecar.items import YichecarItem


class YichecarSpider(scrapy.Spider):
    name = "yichecarSpider"
    allowed_domains = ["bitauto.com"]
    start_urls = [
        "http://api.car.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=chexing&pagetype=masterbrand&objid=0"
    ]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    pattern = re.compile(r'{type:"mb",id:(\d+),name:"([^"]+)",url:"(/tree_chexing/mb_\d+/)",cur:\d+,num:\d+}')
    dbHelper = MysqldbHelper()

    def __init__(self):
        pass

    def parse(self, response):
        """网页内容解析

        :param response:
        :return:
        """
        content = response.body_as_unicode()
        main_url = "http://car.bitauto.com/"
        cleaned_content = content[14:-1]  # get pure json between JsonpCallBack( and )
        print cleaned_content
        main_brands = self.pattern.finditer(cleaned_content)
        sql = "insert into main_brand(`id`,`name`,`url`) values(%s,%s,%s)"
        for match in main_brands:
            item = YichecarItem()
            item['main_brand_id'] = match.group(1).title()
            item['main_brand_name'] = match.group(2).title()
            item['main_brand_url'] = main_url[:-1]+match.group(3).title().lower()
            # print u"id={},name={},url={}".format(match.group(1).title(), match.group(2).title(), main_url0[:-1]+match.group(3).title().lower())
            # save to mysql, one by one
            params = (item['main_brand_id'], item['main_brand_name'], item['main_brand_url'])
            self.dbHelper.insert(sql, params)

            yield item

        pass
