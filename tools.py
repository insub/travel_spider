#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: hotel
@file: util.py
@time: 2019/9/27 13:55
@desc:
'''

import xmltodict
import json
import random
import re
import pprint
import urlparse3


def get_elements_text(element, xpath, join_str=''):

    return join_str.join(element.xpath(xpath)).replace('\n', '').strip()


def get_elements_texts(element, xpath):

    return [i.replace('\n', '').strip() for i in element.xpath(xpath) if i.replace('\n', '').strip() != "" ]


def get_number(str):
    str = str.replace(",", '')
    pattern = re.compile('\d+')
    els = [i for i in re.findall(pattern, str)]
    if len(els) > 0:
        return els[0]


def delete_str(text,pattern_str):
    pattern = re.compile(pattern_str)
    for i in pattern.findall(text):
        text = text.replace(i, '')
    return text


def xml_2_json(xml):
    json_obj = xmltodict.parse(xml, encoding='utf-8')
    json_obj = json.loads(json.dumps(json_obj))
    return json_obj


def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    v = 0
    a = random.randint(5, 18)
    b = random.randint(0, 3)
    while current < distance:
        if current < mid:
            a = a
        else:
            a = -(a + b)
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    track.extend([-i for i in track])
    return track


def is_exist_tag(element, xpath):
    if element.xpath(xpath) is None:
        return False
    else:
        return True


def json_get(text, keys):
    try:
        if isinstance(text, str):
            js = json.loads(text)
        else:
            js = text

        for key in keys:
            js = js.get(key)
        return js
    except Exception as e:
        print(e)
    return ''


def get_cookie(cookie_str, split_char=";"):
    cookie = {}
    for key_value in cookie_str.split(split_char):
        cookie[key_value.split('=')[0].strip()] = key_value.lstrip(key_value.split('=')[0]).replace('=', '',1)
    return cookie


def get_data_from_str(data_str):
    try:
        pattern = "(\d+)"
        m = re.findall(pattern=pattern, string=data_str)
        data_str = m[0]
        import time
        timeArray = time.localtime(int(data_str)/1000)
        return time.strftime("%Y-%m-%d", timeArray)
    except Exception as e:
        print(e)


def remove_tag(content):
    pattern = re.compile("(<.+?>)")
    tags = re.findall(string=content, pattern=pattern)
    for tag in tags:
        content = content.replace(tag, "")
    return content

def get_url_query(url):
    parse = urlparse3.parse_url(url)
    return dict(parse.query)