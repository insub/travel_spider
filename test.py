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

from travel_spider.items import *
from travel_spider.utils import *

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
        return pattern.findall(text)[0]
        # text = text.replace(pattern.findall(text)[0], '').replace(',"pagehtml":','')
        # import json
        # # print(text)
        # jsn = json.loads(text, strict=False)
        # pprint.pprint(jsn)


def qyer_poi_detail():
     url = 'https://place.qyer.com/poi/V2UJYVFkBzJTZVI9/'
     with requests.session() as sess:
         response = sess.get(url)
         print(response.text)
content = {
    'play': '娱乐',
    'scenery': '景点'
}
def lvmama_parse_poi_list(url):
    with requests.session() as sess:
        response = sess.get(url)
        html = HTML(response.text)
        a_list = html.xpath('.//div[@id="viewspot_list"]/dl/dd/div[@class="title"]/a')
        if not a_list:
            a_list = html.xpath('.//div[@id="play_list"]//dl//div[@class="item-info"]//strong/a')
        if not a_list:
            a_list = html.xpath('.//div[@id="view_list"]//dl/dd//a')
        for a in a_list:
            # urls = [url for url in urls if url.startswith('http://www.lvmama.com/lvyou') and not url.endswith('#dianping')]
            # for url in urls:

            url = get_text_by_xpath(a, '@href')
            title = get_text_by_xpath(a, 'text()')

            if url.startswith('http://www.lvmama.com/lvyou/poi'):
                print(url)
            else:
                # 'http://www.lvmama.com/lvyou/d-lasiweijiasi3719.html'
                lase_index = len(url) - url[::-1].index('/')
                for type in content.keys():
                    temp_url = url[:lase_index - 1] + '/' + type + url[lase_index - 1:]
                    print(temp_url)
                    lvmama_parse_poi_list(temp_url)
                    # yield Request(url=url[:lase_index - 1] + '/' + type + url[lase_index - 1:],  meta={'country': response.reqeust.meta.get('country'), 'type': type}, callback=self.parse_poi_list)


def lvmama_poi_detail(url):
    with requests.session() as sess:
        response = sess.get(url)
        html = HTML(response.text)
        item = LvmamaPoiDetailItem()
        item['raw'] = {'html': str(lzma.compress(response.content))}
        if 'sight' in url:
            item['head'] = get_text_by_xpath(html, './/span[@class="crumbs_nav"]/span//text()')
            item['title'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/h2[@class="title"]/text()')
            item['title_en'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/span[@class="title-eng"]/text()')
            item['vcomon'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/i[@class="vcomon-icon"]/text()')
            # item['country'] = response.request.meta.get('country')
            dls = html.xpath('.//dl[@class="poi_bordernone"]')
            for dl in dls:
                dt = get_text_by_xpath(dl, './/dt//text()')
                dd = get_text_by_xpath(dl, './/dt//text()')
                if '简介' in dt:
                    item['poi_brief'] = dd

                elif '景点导览' in dt:
                    item['poi_detail'] = dd

                elif '交通信息' in dt:
                    item['traffic'] = dd

                elif '小贴士' in dt:
                    item['poi_tip_content'] = dd

            dts = html.xpath('.//div[@class="vtop-comment-box fl"]/dl/dt')
            dds = html.xpath('.//div[@class="vtop-comment-box fl"]/dl/dd')
            for dt, dd in zip(dts, dds):
                dt = get_text_by_xpath(dt, './/text()')
                dd = get_text_by_xpath(dd, './/text()')
                if '地　　址' in dt:
                    item['address'] = dd
                elif '游玩时间' in dt:
                    item['playtime'] = dd
                elif '联系电话' in dt:
                    item['phone'] = dd
                elif '门票' in dt:
                    item['ticket'] = dd
                elif '开放时间' in dt:
                    item['open_time'] = dd
                elif '网址' in dt:
                    item['website'] = dd
        elif 'zone' in url:
            item['head'] = get_text_by_xpath(html, './/div[@class="nav clearfix"]/span[@class="crumbs_nav fl"]//text()')
            item['title'] = get_text_by_xpath(html,
                                              './/div[@class="nav_country clearfix"]/div[@class="countryBox fl"]/h1/text()')
            item['title_en'] = get_text_by_xpath(html,
                                                 './/div[@class="nav_country clearfix"]/div[@class="countryBox fl"]/h1/span/text()')
            item['active'] = get_text_by_xpath(html,
                                               './/div[@class="nav_country clearfix"]/div[@class="countryBox fl"]/p[@class="active"]/text()')
            dls = html.xpath('.//div[@class="city_viewBox"]/div[@class="city_view_model"]/div/dl')
            for dl in dls:
                dt = get_text_by_xpath(dl, './/dt//text()')
                dd = get_text_by_xpath(dl, './/dd//text()')
                if '简介' in dt:
                    item['poi_brief'] = dd

                elif '景点导览' in dt:
                    item['poi_detail'] = dd

                elif '交通信息' in dt:
                    item['traffic'] = dd

                elif '小贴士' in dt:
                    item['poi_tip_content'] = dd

            divs = html.xpath('.//dl[@class="city_mapList clearfix"]/dd/div')
            for div in divs:
                dt = get_text_by_xpath(div, './/p[1]//text()')
                dd = get_text_by_xpath(div, './/p[2]//text()')
                if '地址' in dt.replace(' ',''):
                    item['address'] = dd
                elif '游玩时间' in dt:
                    item['playtime'] = dd
                elif '联系电话' in dt:
                    item['phone'] = dd
                elif '门票' in dt:
                    item['ticket'] = dd
                elif '开放时间' in dt:
                    item['open_time'] = dd
                elif '网址' in dt:
                    item['website'] = dd

        # item['url'] = response.request.url
        return item

if __name__ == '__main__':
    url = 'http://www.lvmama.com/lvyou/play/d-meiguo3571.html'
    print(lvmama_parse_poi_list(url))