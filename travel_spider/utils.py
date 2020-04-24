#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: tutorail
@file: utils.py
@time: 2019/2/22 12:07
@desc:
'''
import datetime
import os
import time

import urlparse3

def get_error_log_dir(spider):
    '''
    get the file path for log failed request urls
    :param spider:
    :return:
    '''
    path = spider.settings.get("FAIL_REQUEST_URLS_DIR")
    if path is None:
        path = './'
    return os.path.join(path, spider.name + '.txt')


def write_error_log(spider, item):
    '''
    write failed request urls to file.
    :param spider:
    :param item:
    :return:
    '''
    with open(get_error_log_dir(spider), mode='a') as file:
        file.write('{time} SPIDER:{spider} URL:{url} INFO:{msg}\n'
                   .format(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                           spider=spider.name, url=item['url'], msg=item['msg']))


def get_error_status_code(spider):
    '''
    get request failed code,
    default is 999
    :param spider:
    :return:
    '''
    code = spider.settings.get('ERROR_STATUS_CODE')
    if code is None:
        code = 999
    return code


def get_ts():
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return ts


def get_next_run_time(minutes=30):
    return datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(minutes=minutes), "%Y-%m-%d %H:%M:%S")


def get_date(days = 0, strpt="%Y-%m-%d"):
    delta = datetime.timedelta(days=days)
    return datetime.datetime.strftime(datetime.datetime.now() + delta, strpt)


def get_text_by_xpath(ele, xpath, join_str=""):
    try:
        return join_str.join([i.replace('\n', '').strip() for i in ele.xpath(xpath) if i != ""])
    except Exception as e:
        return ''


def get_url_query(url):
    parse = urlparse3.parse_url(url)
    return dict(parse.query)


def get_cookie(cookie_str, split_char=";"):
    cookie = {}
    for key_value in cookie_str.split(split_char):
        cookie[key_value.split('=')[0].strip()] = key_value.lstrip(key_value.split('=')[0]).replace('=', '',1)
    return cookie


def get_indexof(s, c):
    try:
        return s.index(c)
    except Exception as e:
        return -1


if __name__ == '__main__':
    s = "镇美景酒店Town View Hotel"

    print(s[get_indexof(s, '(')+1:-1])