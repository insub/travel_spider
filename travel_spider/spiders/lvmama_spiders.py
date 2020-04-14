#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: travel_spider
@file: lvmama_spiders.py
@time: 2020/4/13 13:22
@desc:
'''
import copy
from itertools import product
import math
import re

import json
from lxml.etree import HTML
import lzma
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from urllib.parse import urlencode

from travel_spider.country import lvmanma_countries
from travel_spider.utils import get_text_by_xpath
from travel_spider.items import LvmamaPoiDetailItem, LvmamaPoiItem


class LvmamaSpider(RedisSpider):
    name = 'lvmama_spider'
    custom_settings = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'http://www.lvmama.com',
        'referer': 'http://www.lvmama.com/lvyou/scenery/select-3571-a6781.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    content = {
        'play': {'url': 'http://www.lvmama.com/lvyou/dest_content/AjaxGetPlayList?',
                 'data': {'page': 1,
                    'dest_id': ''
                },'page_per_count': 20},

        'scenery': {'url': 'http://www.lvmama.com/lvyou/ajax/getNewViewList?',
                 'data':{'page_num': 1,
                        'dest_id': "",
                        'base_id': 1,
                        'request_uri': '/lvyou/scenery/'
                },
                    'page_per_count': 10},
    }

    def start_requests(self):
        url = 'http://www.lvmama.com/lvyou/{type}/{country}'
        for country, (type, value) in product(lvmanma_countries, self.content.items()):
            dest_id_pattern = re.compile('(\d+)')
            dest_id = dest_id_pattern.findall(country)[-1]
            data = copy.deepcopy(value.get('data'))
            data['dest_id'] = dest_id
            page_per_count = value.get('page_per_count')
            if 'request_uri' in data:
                data['request_uri'] = data['request_uri'] + country
            # url = value.get('url') + urlencode(data)

            yield Request(url=url.format(type=type, country=country), dont_filter=True,
                          meta={'country': country, 'request_uri': country,
                                'dest_id': dest_id,  'type': type, 'level': 'country', 'page_per_count': page_per_count},
                          callback=self.parse)

    def parse(self, response):
        # 获取 dest_id, base_id
        # 获取页码数

        html = HTML(response.text)
        meta = response.request.meta
        num_pattern = re.compile('(\d+)')
        count_info = get_text_by_xpath(html, './/div[@class="wy_state_page"]/p//text()')
        total_count = num_pattern.findall(count_info)[-1]
        page_num = 1
        if total_count.isdigit():
            page_per_count = meta.get('page_per_count')
            page_num = math.ceil(int(total_count)/page_per_count)
        # page_num = max([int(i) for i in page_nums if i.isdigit()])
        view_list = html.xpath('.//div[@id="view_list"]')
        if view_list:
            for request in self.parse_play_detail(html, meta):
                yield request
            return

        type = meta.get('type')
        dest_id = meta.get('dest_id')
        for i in range(1, page_num + 1):
            if type == 'play' and meta.get('level') == 'country':
                data = {
                    'page': i,
                    'dest_id': dest_id
                }
                yield Request(url="http://www.lvmama.com/lvyou/dest_content/AjaxGetPlayList?"+urlencode(data), meta=meta, callback=self.parse_play_list)

            elif type == 'play' and meta.get('level') != 'country':
                data = {'page': i,
                        'dest_id': dest_id,
                        'search_key': '',
                        'request_uri': '/lvyou/play/' + meta.get('request_uri'),
                        'type': type}
                yield Request(url="http://www.lvmama.com/lvyou/dest_content/AjaxGetViewSpotList?" + urlencode(data), meta=meta, callback=self.parse_play_list2)

            elif type == 'scenery':
                base_id_pattern = re.compile('base_id  :"(\d+)",')
                base_id = base_id_pattern.findall(response.text)[-1]
                data = {'page_num': i,
                        'dest_id': dest_id,
                        'base_id': base_id,
                        'request_uri': '/lvyou/scenery/' + meta.get('request_uri')
                }
                yield Request(url='http://www.lvmama.com/lvyou/ajax/getNewViewList?'+urlencode(data), meta=meta, callback=self.parse_view_list)

    def parse_view_list(self, response):
        # 景点列表解析

        jsn = json.loads(response.text)
        meta = response.request.meta
        item = LvmamaPoiItem()
        item['raw'] = {'meta': meta, 'content': jsn}
        yield item

        meta['level'] = 'poi'
        html = HTML(jsn.get('data'))
        a_list = html.xpath('.//dl/dd/div[@class="title"]/a')
        for a in a_list:
            url = get_text_by_xpath(a, '@href')
            if url.startswith('http://www.lvmama.com/lvyou/poi') and not url.endswith('#dianping'):
                url = get_text_by_xpath(a, '@href')
                yield Request(url=url, meta=meta, callback=self.parse_poi)

    def parse_play_list(self, response):
        # country 层面的playlist
        jsn = json.loads(response.text)
        item = LvmamaPoiItem()
        meta = response.request.meta
        item['raw'] = {'meta': meta, 'content': jsn}
        yield item

        meta['level'] = 'city'
        html = HTML(jsn.get('data').get('html'))
        a_list = html.xpath('.//dl//div[@class="item-info"]//strong/a')
        for a in a_list:
            url = get_text_by_xpath(a, '@href')
            if url.startswith('http://www.lvmama.com/lvyou') and not url.endswith('#dianping'):
                url = get_text_by_xpath(a, '@href')
                meta['request_uri'] = url.replace("http://www.lvmama.com/lvyou/", '')
                yield Request(url=url, meta=meta, callback=self.parse)

    def parse_play_list2(self, response):
        ## city 层面的playlist
        jsn = json.loads(response.text)
        item = LvmamaPoiItem()
        meta = response.request.meta
        item['raw'] = {'meta': meta, 'content': jsn}
        yield item

        meta['level'] = 'poi'
        html = HTML(jsn.get('data').get('html'))
        for request in self.parse_play_detail(html, meta):
            yield request
        # a_list = html.xpath('.//dl/dt/a')
        # for a in a_list:
        #     url = get_text_by_xpath(a, '@href')
        #     meta['request_uri'] = url.replace("http://www.lvmama.com/lvyou/poi/", '')
        #     yield Request(url=url, meta=meta, callback=self.parse_poi)

    def parse_play_detail(self, html, meta):
        a_list = html.xpath('.//dl/dt/a')
        result = []
        for a in a_list:
            url = get_text_by_xpath(a, '@href')
            meta['request_uri'] = url.replace("http://www.lvmama.com/lvyou/poi/", '')
            result.append(Request(url=url, meta=meta, callback=self.parse_poi))
        return result

    def parse_poi(self, response):
        html = HTML(response.text)
        item = LvmamaPoiDetailItem()
        meta = response.request.meta
        item['raw'] = {'html': str(lzma.compress(response.body)), 'meta': meta}
        url = response.request.url
        item['url'] = url
        item['country'] = meta['country']

        if 'sight' in url:
            item['head'] = get_text_by_xpath(html, './/span[@class="crumbs_nav"]/span//text()')
            item['title'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/h2[@class="title"]/text()')
            item['title_en'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/span[@class="title-eng"]/text()')
            item['vcomon'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/i[@class="vcomon-icon"]/text()')

            dls = html.xpath('.//dl[@class="poi_bordernone"]')
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
        yield item

