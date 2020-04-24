#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: lab
@file: selenium.py
@time: 2020/4/24 16:57
@desc:
'''
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--proxy-server=http://127.0.0.1:8080')

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
                          options=chrome_options)

while True:
    driver.get('https://hotels.ctrip.com/international/cairo332')
    driver.
    driver.delete_all_cookies()

