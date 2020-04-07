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

url = 'https://www.mafengwo.cn/poi/5424045.html'
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

