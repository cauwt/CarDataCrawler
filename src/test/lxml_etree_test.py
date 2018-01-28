#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# file: lxml_etree_test
# author: eva
# date: 2018/1/28
# version: 
# description:
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    from lxml import etree
    text = '''
        <div>
            <ul>
                 <li class="item-0"><a href="link1.html">first item</a></li>
                 <li class="item-1"><a href="link2.html">second item</a></li>
                 <li class="item-inactive"><a href="link3.html">third item</a></li>
                 <li class="item-1"><a href="link4.html">fourth item</a></li>
                 <li class="item-0"><a href="link5.html">fifth item</a>
             </ul>
         </div>
        '''
    html = etree.HTML(text)
    result = html.xpath('//li[last()-1]/a')
    print type(result[0])
    print result[0].text

    result = html.xpath('//li[last()]/a/@href')
    print type(result[0])
    print result[0]
