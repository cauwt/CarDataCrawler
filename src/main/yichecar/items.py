# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YichecarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_brand_id = scrapy.Field()
    main_brand_name = scrapy.Field()
    main_brand_url = scrapy.Field()

if __name__ == '__main__':
    pass
