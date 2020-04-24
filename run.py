#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: travel_spider
@file: run.py
@time: 2020/4/10 14:58
@desc:
'''
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from travel_spider.spiders.qyer_spiders import QyerSpider


def main():
    process = CrawlerProcess()  
    process.crawl(QyerSpider)
    process.start()


if __name__ == '__main__':
    # cmdline.execute('scrapy crawl stock_sina_trade_detail_per_day'.split())
    cmdline.execute('scrapy crawl ctrip_spider'.split())
