# -*- coding: utf-8 -*-
import scrapy
import urllib2
from lxml import etree
import os
from items import ReadingSpiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ReadingspiderSpider(scrapy.Spider):
    name = 'bigreadingSpider'#爬虫名
    allowed_domains = ['http://www.xinbiquge.com/']#总域
    start_urls = ['http://www.bxquge.com/paihangbang/']#起始页


    def parse(self, response):

        sel = scrapy.selector.Selector(response)#解析域
        for i in range(2,10):
            path = '//*[@id="main"]/table[' +str(i)+ ']/tbody/tr[1]/td[2]/span'#排行榜路径
            sites = sel.xpath(path)
            items = []
            for site in sites:#按9个排行榜爬取
                item = ReadingSpiderItem()
                path_list_name = '//*[@id="main"]/table[' +str(i)+ ']/tbody/tr[1]/td[2]/span/text()'
                item['list_name'] = site.xpath(path_list_name).extract()#排行榜名称

                try:
                    os.mkdir(item['list_name'][0])
                except IOError:
                    pass
                os.chdir(item['list_name'][0])

                for li in range(1,21):
                    title = '//*[@id="tb' + str(i-1) + '-1"]/ul/li['+str(li)+']/a/text()'
                    item['name'] = site.xpath(title).extract()#书名
                    url = 'http://www.bxquge.com/'
                    path_link = '//*[@id="tb'+ str(i-1) +'-1"]/ul/li[' + str(li) + ']/a/@href'#书目链接
                    item['link'] = site.xpath(path_link).extract()
                    full_url = url + item['link'][0]

                    headers = {'User-Agent':
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                                   (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
                    #request = urllib2.Request(''.join(item['link']),headers=headers)
                    request = urllib2.Request(full_url, headers=headers)

                    try:
                        os.mkdir(item['name'][0])
                    except IOError:
                        pass
                    os.chdir(item['name'][0])

                    response = urllib2.urlopen(request).read().decode('utf-8')
                    tree = etree.HTML(response)
                    for j in range(1,11):
                        path_title = '//*[@id="list"]/dl/dd['+ str(j) +']/a/text()'
                        item['title'] = tree.xpath(path_title)#章节名

                        path_words_page = '//*[@id="list"]/dl/dd['+ str(j) +']/a/@href'
                        word_page = tree.xpath(path_words_page)
                        try:
                            url_words = full_url +  word_page[0]
                            request_words = urllib2.Request(url_words,headers=headers)
                            response_words = urllib2.urlopen(request_words).read().decode('utf-8')
                            tree_words = etree.HTML(response_words)
                            path_words = '//*[@id="content"]/text()'
                            item['words'] = tree_words.xpath(path_words)#前20章内容
                        except urllib2.HTTPError:
                            pass
                        items.append(item)

                        try:
                            filename = r''.join(item['title'][0]) + '.json'
                            with open(filename,"a+") as f:
                                a = ''.join(item['title'])
                                b = ''.join(item['words'])
                                f.write(a)
                                f.write(b)
                        except IOError:
                            pass

                    path_now = os.getcwd()
                    path_last = os.path.dirname(path_now)
                    os.chdir(path_last)

                path_now = os.getcwd()
                path_last = os.path.dirname(path_now)
                os.chdir(path_last)

'''
                    contents = urllib.request.urlopen(item["words"])
                    responses = contents.read().decode("utf-8")
                    trees = etree.HTML(responses)
                    title = trees.xpath('//div[@class="readAreaBox content"]/h1/text()')
                    word = trees.xpath("/html/body/div[4]/div[2]/div[2]/div[1]/div[2]/text()")
                    print(''.join(title)
 
                    scrapy crawl bigreadingSpider -s FEED_EXPORT_ENCODING=utf-8
 
'''