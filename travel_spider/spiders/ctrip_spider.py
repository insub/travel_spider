#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: travel_spider
@file: ctrip_spider.py
@time: 2020/4/24 11:21
@desc: 携程网
'''
import copy
import lxml
import lzma
import json
import re


import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request


from travel_spider.country import ctrip_cities
from travel_spider.items import CtripHoteItem, CtripHotelMDBITem
from travel_spider.utils import get_indexof

class CtripSpider(RedisSpider):

    name = "ctrip_spider"

    URL = "https://hotels.ctrip.com/international/tool/AjaxHotelList.aspx"
    DIGIT_PATTERN = re.compile("(\d+)")

    DATA = {'checkIn': '2020-04-24',
     'checkOut': '2020-04-25',
     'destinationType': '1',
     'IsSuperiorCity': '1',
     'cityId': '3471',
     'cityPY': 'hurghada',
     'rooms': '1',
     'childNum': '1',
     'roomQuantity': '1',
     'pageIndex': '1',
     'keyword': '',
     'keywordType': '',
     'LandmarkId': '',
     'districtId': '',
     'zone': '',
     'metrostation': '',
     'metroline': '',
     'price': '',
     'star': '',
     'equip': '',
     'brand': '',
     'group': '',
     'fea': '',
     'htype': '',
     'promotionf': '',
     'coupon': '',
     'a': '',
     'orderby': '2',
     'ordertype': '1',
     'isAirport': '0',
     'hotelID': '',
     'priceSwitch': '',
     'lat': '',
     'lon': '',
     'clearHotelName': '',
     'InitPageLoad': 'F',
     'disCountItemSelected': '[]',
     'lat_cityCenter': '30.0444196',
     'lon_cityCenter': '31.2357116',
     'searchByDisLenovoHotelId': '0',
     'TopSetHotelListFromUrl': '',
     'pageid': '102102',
     'eleven': '76980900c485f24c274b23a3bc6199f495d9bf7bdff252729409f140086a0404_1852097478',
     'hasMapLoaded': 'T',
     'IsNeedHermesRefresh': 'T',
     'preHotelIdList': '',
     'IsPreloadAjax': 'F',
     }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "referer": "https://hotels.ctrip.com/international/cairo332",
        "origin": "https://hotels.ctrip.com",
        'accept-language': 'zh-CN,zh;q=0.9',
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "IntlVID=110106-43a0f2d8-5fa2-4675-a4f2-363662277b43; ASP.NET_SessionSvc=MTAuMjUuMTY3LjQ4fDkwOTB8b3V5YW5nfGRlZmF1bHR8MTU4NzAzNTgyMjY3OA; _abtest_userid=fd4fd656-baec-4872-9817-4700f4cd5998; magicid=s3PairXrLrEkr+CMhN9S0KqeV5F7j+HUrS6U/DzEcf7BaLSQv4yIN4/TI76Mhhde; clientid=51482090210776652021; IntHotelCityID=splitsplitsplit2020-04-24split2020-04-25splitsplitsplit1split1split1; _bfa=1.1587629092942.355wwh.1.1587629092942.1587629092942.1.1; _bfs=1.1; hoteluuid=16LXCtMgpNHdu7lS; hoteluuidkeys=OpHy5tYcDe8sJX8WXYOYdSYgDEgYOYf1e9PEn4j1tW1Y6YzZjZpi5zeGNybYoY5dynGwL8I9tW5Y0YS1RAaRZdvlpj5YDYTOvpsYfbyAOjQ1vfhe6zeqgjhayfYzYZGvTOvA3YlkwP9jgXeF5iZ5Y9YTYzYMYS9vnteQ6YMpiHsYHY5YaYlYNaEO8KLtwtai15RSpj4rmTYThJ0pyNrS4YM7W1HvZSxz4e3HYfzxpHxNzYpniAqwmOjtOEFSJ1LWpHj1rDzJfliGLwL0vbtRlHjFHYsDjZrX6yHhil7wmgROXESDj1FxOdxXMEsUE3HEzaWbDeTnw5SEpojt8eaAiZQYsQr8pekaedAxXziSdiM4xAnWNSj60ebOwGqKo5wT3iscRB6jdgesnEb6yBfvqPiHgEkgyGmv1sKktEt0Kk8wP7idSRMkjNrSUYTQJQSylr6ZjpteTAjmfKLqjBhw91xDqxLsxZNxDfEXgE6oEF7WBheMZwPNEqUjBceD9i1LYSsrHNEDdyTZvPki6LEspygNvm8KDmWzLEsUjUTeQqxtnjsr7LENmWGpebgjzNYLdjN1xbXxs6xpAxsaEAHEZpEp3WbseNAwdzElAjBHeFUiT6YQdrNUe1te9dYO6EtmwSaWO6iddKSZEPhEl8EgQWtoe7gw5FEmlj4nebcio7YThraZes5eDAEUZYQPEn5wPZWlhi8YfYs9YHSiM4iSmidzjpYSYdFEa7jUOjlbJdDjbBwOgy46w4Y1Ym1RkMJzOjphylGw4nYhmv3OWUBvGQiN8Rptyf9YfYcY3URUOwkoIDDxGSESqjM5rL6xOFEfZWhbv1MyAGvpZy93WzaJzYtYoDR59JPSjZTyclwSHYZ3vmlWoavM3YT4voMElOYlYGYkPjOPwMUvNH; __utma=13090024.784265839.1587629093.1587629093.1587629093.1; __utmc=13090024; __utmz=13090024.1587629093.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=13090024.2.10.1587629093; MKT_CKID=1587629099132.nz26j.cb5i; MKT_CKID_LMT=1587629099133; __zpspc=9.1.1587629099.1587629099.1%234%7C%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.463871537.1587629099150.1587629099150.1587629099150.1587629099150.1587629099150.0.0.0.1.1; MKT_Pagesource=PC; appFloatCnt=1; _ga=GA1.2.784265839.1587629093; _gid=GA1.2.1116243172.1587629099; _gat=1; hotelhst=1261406863; _RF1=101.95.169.14; _RSG=xtakgKIUZNCpgd.ugDbGu9; _RDG=28aaa3ccf0de7f27de0e6c746da11db494; _RGUID=c5e37925-2aba-4dfb-9e10-94dab8fa7ab3; IntlIOI=F; _bfi=p1%3D102102%26p2%3D0%26v1%3D1%26v2%3D0"
    }

    def start_requests(self):
        """:param
            城市为种子进行
        """
        for city in ctrip_cities:
            city_id = self.DIGIT_PATTERN.findall(city)[-1]
            meta = dict()
            meta['city'] = city
            meta['city_id'] = city_id
            data = copy.deepcopy(self.DATA)
            data['cityId'] = city_id
            data['cityPY'] = city.replace(city_id, '')
            meta['data'] = data
            meta['page'] = 1

            yield scrapy.FormRequest(self.URL, formdata=data, meta=meta, headers=self.headers, dont_filter=True, callback=self.parse)

    def parse(self, response):
        """:param
        解析返回数据
        1. 获取酒店条数，对每页生成url
        2.解析酒店记录
        """
        meta = response.request.meta
        mgo_item = CtripHotelMDBITem()
        mgo_item['raw'] = {'content': str(lzma.compress(response.body)), 'meta': meta}
        yield mgo_item

        jsn = json.loads(response.text)

        # html = lxml.etree.HTML(jsn['hotelListHtml'])
        hotel_list = jsn['HotelPositionJSON']
        # hotel_list = html.xpath('.//div[@class="J_hlist_item hlist_item"]')
        for hotel in hotel_list:
            item = CtripHoteItem()
            item['title'] = hotel['name']
            ix = get_indexof(hotel['name'], '(')
            item['title_en'] = hotel['name'][ix + 1:-1] if ix != -1 else ''
            item['city'] = meta.get('city')
            item['city_id'] = meta.get('city_id')
            item['url'] = hotel['url']
            yield item

        if meta['page'] == 1:
            page = jsn.get('totalPage')
            for i in range(2, page+1):
                data = meta.get('data')
                data['pageIndex'] = str(i)
                meta['page'] = i
                yield scrapy.FormRequest(self.URL, formdata=data, meta=meta,  dont_filter=True, headers=self.headers, callback=self.parse)
