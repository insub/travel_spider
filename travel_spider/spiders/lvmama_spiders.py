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
from lxml.etree import HTML
import lzma
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request

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
        'play': '娱乐',
        'scenery': '景点'
    }

    def start_requests(self):
        url = 'http://www.lvmama.com/lvyou/{type}/{country}'
        for country, type in zip(lvmanma_countries, self.content.keys()):
            yield Request(url=url.format(type=type, country=country), dont_filter=True, meta={'country': country, 'type': type}, callback=self.parse_poi_list)

    def parse_poi_list(self, response):
        html = HTML(response.text)
        a_list = html.xpath('.//div[@id="viewspot_list"]/dl/dd/div[@class="title"]/a')

        if not a_list:
            a_list = html.xpath('.//div[@id="play_list"]//dl//div[@class="item-info"]//strong/a')
        if not a_list:
            a_list = html.xpath('.//div[@id="view_list"]//dl/dd//a')
        for a in a_list:
            url = get_text_by_xpath(a, '@href')
            title = get_text_by_xpath(a, 'text()')
            if not url.startswith('http://www.lvmama.com') or url.endswith('#dianping'):
                continue
            item = LvmamaPoiItem()
            item['raw'] = {'title': title, 'url': url}
            yield item

            if url.startswith('http://www.lvmama.com/lvyou/poi'):
                yield Request(url=url, meta=response.request.meta, callback=self.parse_poi)
            else:
                # 'http://www.lvmama.com/lvyou/d-lasiweijiasi3719.html'
                lase_index = len(url) - url[::-1].index('/')
                for type in self.content.keys():
                    yield Request(url=url[:lase_index - 1] + '/' + type + url[lase_index - 1:],  meta={'country': response.request.meta.get('country'), 'type': type}, callback=self.parse_poi_list)

    def parse_poi(self, response):
        html = HTML(response.text)
        item = LvmamaPoiDetailItem()
        item['raw'] = {'html': str(lzma.compress(response.body))}
        url = response.request.url
        item['url'] = url
        item['country'] = response.request.meta.get('country')


        if 'sight' in url:
            item['head'] = get_text_by_xpath(html, './/span[@class="crumbs_nav"]/span//text()')
            item['title'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/h2[@class="title"]/text()')
            item['title_en'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/span[@class="title-eng"]/text()')
            item['vcomon'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/i[@class="vcomon-icon"]/text()')


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
        yield item

