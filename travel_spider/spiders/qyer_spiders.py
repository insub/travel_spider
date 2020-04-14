#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: travel_spider
@file: spiders.py
@time: 2020/4/10 9:40
@desc:
"""

import re
from urllib.parse import urlencode

import execjs
from lxml.etree import HTML
import lzma
import json
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request

from travel_spider import utils
from travel_spider import items
from travel_spider.country import  qyer_countries

class QyerSpider(RedisSpider):
    '''
    穷游网站
    '''

    name = 'qyer_spider'

    custom_settings = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'https://place.qyer.com',
        'referer': 'https://place.qyer.com/dubai/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    def start_requests(self):
        """
        传入地点的url
        eg:https://place.qyer.com/hong-kong/sight/
        """
        url = "https://place.qyer.com/{country}/citylist-0-0-1/"
        for country in qyer_countries:
            yield Request(url=url.format(country=country), dont_filter=False, callback=self.parse_city)
            # yield Request(url='https://place.qyer.com/hong-kong/sight/', dont_filter=False)

    def parse_city(self, response):
        html = HTML(response.text)
        urls = html.xpath('.//ul[@class="plcCitylist"]/li/h3/a/@href')
        for url, suffix in zip(urls, ['sight/', 'activity/']):
            yield Request(url='http:'+url+suffix, callback=self.parse)

    def get_page_num(self, html):
        page_nums = html.xpath('.//div[@class="ui_page"]/a/@data-page')
        page_nums = [int(i) for i in page_nums if i.isdigit()]
        page_num = max(page_nums)
        return page_num

    def parse(self, response):
        """:param
            解析旅游点的列表
          1.获取地点的pid
          2.获取旅游列表的页码
          3.返回ajax网址
          eg:https://place.qyer.com/dubai/sight/
        """
        url = 'https://place.qyer.com/poi.php?'

        # 获取参数
        pattern = re.compile('var PLACE ([\d\D]+?);')
        place = pattern.findall(response.text)[0].replace('= PLACE || ', '')
        place = execjs.eval(place)
        # 获取页码
        html = HTML(response.text)

        page_num = self.get_page_num(html)

        poi_sort = utils.get_text_by_xpath(html, './/p[@id="poiSort"]/a[@class="current"]/@data-id')
        # TODO
        if page_num < 100:
            for i in range(1, page_num+1):
                param = {'action': 'list_json',
                         'haslastm': 'false',
                         'isnominate': '-1',
                         'page': i,
                         'pid': place['PID'],
                         'rank': '6',
                         'sort': poi_sort,
                         'subsort': 'all',
                         'type': place['TYPE']}
                print('爬取第{} 页'.format(i))
                yield Request(url=url+urlencode(param), callback=self.parse_poi_list)
        else:
            subsorts = html.xpath('.//li[@id="poiSubsort"]/p[@id="poiSortLabels"]/a/@data-id')
            for subsort in subsorts:
                if subsort == '0':
                    continue
                param = {'action': 'list_json',
                         'haslastm': 'false',
                         'isnominate': '-1',
                         'page': 1,
                         'pid': place['PID'],
                         'rank': '6',
                         'sort': poi_sort,
                         'subsort': subsort,
                         'type': place['TYPE']}
                # print('爬取第{} 页'.format(1))
                yield Request(url=url + urlencode(param), meta={'param': param}, callback=self.pares_poi_subpage)

    def pares_poi_subpage(self, response):
        url = 'https://place.qyer.com/poi.php?'
        text = response.body.decode('unicode-escape').replace('\n', '').replace('\r', '')
        pattern = re.compile('"pagehtml":(.*)}}')
        html = HTML(pattern.findall(text)[0])
        page_num = self.get_page_num(html)
        param = response.request.meta.get('param')
        for i in range(1, page_num + 1):
            param = {'action': 'list_json',
                     'haslastm': 'false',
                     'isnominate': '-1',
                     'page': i,
                     'pid': param.get('pid'),
                     'rank': '6',
                     'sort': param.get('sort'),
                     'subsort': param.get('subsort'),
                     'type': param.get('type')}
            print('爬取第{} 页'.format(i))
            yield Request(url=url + urlencode(param), meta={'param': param}, callback=self.parse_poi_list)

    def parse_poi_list(self, response):
        """
         旅游景json数据解析
         eg:https://place.qyer.com/poi.php?action=list_json&page=3&type=city&pid=6406&sort=32&subsort=all&isnominate=-1&haslastm=false&rank=6
        """
        text = response.body.decode('unicode-escape').replace('\n', '').replace('\r', '')
        pattern = re.compile('"pagehtml":(.*)}}')
        text = text.replace(pattern.findall(text)[0], '').replace(',"pagehtml":', '')
        jsn = json.loads(text)
        for content in jsn.get('data').get('list'):
            item = items.PoiItem()
            item['raw'] = content
            yield item
            yield Request('http:' + content.get('url'), meta={'id': content.get('id'), 'catename':content.get('catename')}, callback=self.parse_poi_detail)

    def parse_poi_detail(self, response):
        """
        旅游景点解析
        eg:https://place.qyer.com/poi/V2UJYVFkBzJTZVI9/
        """
        html = HTML(response.text)
        item = items.PoiDetailItem()
        item['raw'] = {'html': str(lzma.compress(response.body))}

        item['url'] = response.request.url
        item['id'] = response.request.meta.get('id')
        item['catename'] = response.request.meta.get('catename')
        item['head'] = utils.get_text_by_xpath(html, './/div[@class="qyer_head_crumb"]/span//text()')
        item['title'] = utils.get_text_by_xpath(html, './/div[@class="poi-largeTit"]/h1[@class="cn"]//text()')
        item['title_en'] = utils.get_text_by_xpath(html, './/div[@class="poi-largeTit"]/h1[@class="en"]//text()')
        item['rank'] = utils.get_text_by_xpath(html, './/div[@class="infos"]//ul/li[@class="rank"]/span//text()')
        item['poi_detail'] = utils.get_text_by_xpath(html, './/div[@class="compo-detail-info"]/div[@class="poi-detail"]//text()')
        item['poi_tips'] = utils.get_text_by_xpath(html, './/div[@class="compo-detail-info"]/ul[@class="poi-tips"]//text()')
        lis = html.xpath('.//div[@class="compo-detail-info"]/ul[@class="poi-tips"]/li')
        for li in lis:
            title = utils.get_text_by_xpath(li, './/span[@class="title"]/text()')
            content = utils.get_text_by_xpath(li, './/div[@class="content"]//text()')
            if '地址' in title:
                item['address'] = content
            elif '到达方式' in title:
                item['arrive_method'] = content
            elif '开放时间' in title:
                item['open_time'] = content
            elif '门票' in title:
                item['ticket'] = content
            elif '电话' in title:
                item['phone'] = content
            elif '网址' in title:
                item['website'] = content
        item['poi_tip_content'] = utils.get_text_by_xpath(html, './/div[@class="compo-detail-info"]/div[@class="poi-tipContent"]//text()')
        yield item
