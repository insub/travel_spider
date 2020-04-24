#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: travel_spider
@file: haoqiao_spider.py
@time: 2020/4/23 11:08
@desc:
'''
from lxml.etree import HTML
import re

import math
import json
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
import lzma

from travel_spider.country import haoqiao_cities
from travel_spider.items import HaoqiaoItem, HaoqiaoMDBItem
from travel_spider.utils import get_text_by_xpath


class HaoqiaoSpider(RedisSpider):

    """
    :param
    好巧网站
    """
    name = 'haoqiao_spider'
    HEADERS = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "referer": "https://www.haoqiao.com/palmcove_c1618",
            'accept-language': 'zh-CN,zh;q=0.9',
            "x-requested-with": "XMLHttpRequest",
    }

    PAGE_URL ='https://www.haoqiao.com/hotellist?city={dest_id}&hq_language=zh-CN&page={page}&checkin=2020-04-24&checkout=2020-04-25&room=1&adult=2&child=0&child_age=&citizenship=CN&token=&sequence=web_1587605108899_525987/hotellist?city=1618&hq_language=zh-CN&page={page}&checkin=2020-04-24&checkout=2020-04-25&room=1&adult=2&child=0&child_age=&citizenship=CN&token=&sequence=web_1587605108899_525987&is_refresh=1&req_type=ajax&vt=&hash=&timestamp='
    HOME_URL = "https://www.haoqiao.com/{city}"
    DIGIT_PATTERN = re.compile("(\d+)")

    def start_requests(self):

        for city in haoqiao_cities:
            dest_id = self.DIGIT_PATTERN.findall(city)[-1]
            meta = dict()
            meta['dest_id'] = dest_id
            meta['page'] = 1
            meta['city_id'] = city
            yield Request(self.HOME_URL.format(city=city), meta=meta)

    def parse(self, response):
        """
        解析首页获取所在城市
        产生列表请求的种子
        """

        meta = response.request.meta
        dest_id = meta['dest_id']

        html = HTML(response.text)
        city = html.xpath('.//input[@id="J_city"]/@value')[-1]
        meta['city'] = city

        yield Request(self.PAGE_URL.format(dest_id=dest_id, page=1), headers=self.HEADERS, meta=meta, callback=self.parse_items)

    def parse_items(self, response):
        """
        :param
        对于列表的解析
        """

        meta = response.request.meta
        page = meta['page']

        jsn = json.loads(response.text)

        # 翻页
        if page == 1:
            result_number = jsn['result_number']
            count_per_page = 10  # 没有一页的记录数量
            pages = math.ceil(result_number/count_per_page)
            for page in range(2, pages + 1):
                meta['page'] = page
                yield Request(self.PAGE_URL.format(dest_id=meta.get('dest_id'), page=page), meta=meta, callback=self.parse_items)
        # 提取记录
        mdb_item = HaoqiaoMDBItem()
        mdb_item['raw'] = {'content': str(lzma.compress(response.body)), 'meta': meta}
        yield mdb_item

        html = HTML(jsn['list'])
        lis = html.xpath('.//li[@class="J_hotel_list"]')
        for li in lis:
            item = HaoqiaoItem()
            item['title'] = get_text_by_xpath(li, './/div[@class="hotel-l-t f20 t-333 fl"]/text()')
            item['title_en'] = get_text_by_xpath(li,  './/div[@class="hotel-l-t f20 t-333 fl"]/span/text()')
            item['city_id'] = meta['city_id']
            item['city'] = meta['city']
            item['url'] = get_text_by_xpath(li,  './/a[1]/@href')
            yield item

