#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: travel_spider
@file: test.py
@time: 2020/4/7 16:36
@desc:
'''
import requests
import chardet
import pprint
import lzma


def mafengwo():
    url = 'lhttps://www.mafengwo.cn/poi/5424045.htm'
    with requests.session() as sess:
        cookies = {	"__jsl_clearance": "1586249921.306|0|F+ip6QkG7T0I6qxPv0c7YzfQI0I=",
        "__jsluid_s": "d1469daefcbad9beeda86a10788ca6ab",
        }
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                      "Connection": "keep-alive",
                      "Host": "www.mafengwo.cn",
                      "TE": "Trailers",
                      'Cookie': '__jsluid_s=d1469daefcbad9beeda86a10788ca6ab; __jsl_clearance=1586249921.306|0|F%2Bip6QkG7T0I6qxPv0c7YzfQI0I%3D',
                      "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"
        }

        res = sess.get(url, cookies=cookies, headers=headers)
        code = chardet.detect(res.content)

        # print(res.content.decode(code.get('encoding','utf-8')))
        print(res.text)
import re
from  lxml.etree import HTML
def qyer():
    url = 'https://place.qyer.com/dubai/sight/'
    with requests.session() as sess:
        response = sess.get(url)
        # print(response.text)
        # pattern = re.compile('var PLACE ([\d\D]+?)};')
        # print(pattern.findall(response.text))

        html = HTML(response.text)
        #
        # els = html.xpath('div[@class="ui_page"/a/@data-page')
        # print(els)
        print(lzma.compress(response.content))


def qyer_poi_list():
    url = 'https://place.qyer.com/poi.php?action=list_json&page=3&type=city&pid=6406&sort=32&subsort=all&isnominate=-1&haslastm=false&rank=7'
    with requests.session() as sess:
        response = sess.get(url)
        # print(response.text)
        # print(chardet.detect(response.content))

        text = response.content.decode('unicode-escape').replace('\n', '').replace('\r', '')
        pattern = re.compile('"pagehtml":(.*)}}')
        text = text.replace(pattern.findall(text)[0], '').replace(',"pagehtml":','')
        import json
        # print(text)
        jsn = json.loads(text, strict=False)
        pprint.pprint(jsn)


def qyer_poi_detail():
     url = 'https://place.qyer.com/poi/V2UJYVFkBzJTZVI9/'
     with requests.session() as sess:
         response = sess.get(url)
         print(response.text)


if __name__ == '__main__':
    # qyer_poi_detail()

    # com = lzma.compress(b'https://place.qyer.com/poi/V2UJYVFkBzJTZVI9/')
    # print(type(com))
    # print(str(com))
    # # print(lzma.decompress(com))
    # # qyer()
    # print(type(eval(str(com))))
    # from travel_spider.items import PoiDetailItem
    # item = PoiDetailItem()
    # item['content'] ='content'
    # item['title'] = 'title'
    # print(item)
    # del item['content']
    # print(item.keys())
    qyer_poi_list()