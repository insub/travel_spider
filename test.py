#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: xuxingyuan
@license: (C) Copyright 2013-2018, Node Supply Chain Manager Corporation Limited.
@software: travel_spider
@file: test.py
@time: 2019/4/7 16:36
@desc:
'''
import requests
import chardet
import pprint
import lzma

from travel_spider.items import *
from travel_spider.utils import *


def mafengwo():
    url = 'lhttps://www.mafengwo.cn/poi/5424045.htm'
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
import re
from  lxml.etree import HTML
def qyer():
    url = 'https://place.qyer.com/dubai/sight/'
    with requests.session() as sess:
        response = sess.get(url)
        # print(response.text)
        # pattern = re.compile('var PLACE ([\d\D]+?)};')
        # print(pattern.findall(response.text))

        html = HTML(response.text)
        #
        # els = html.xpath('div[@class="ui_page"/a/@data-page')
        # print(els)
        print(lzma.compress(response.content))


def qyer_poi_list():
    url = 'https://place.qyer.com/poi.php?action=list_json&page=3&type=city&pid=6406&sort=32&subsort=all&isnominate=-1&haslastm=false&rank=7'
    with requests.session() as sess:
        response = sess.get(url)
        # print(response.text)
        # print(chardet.detect(response.content))

        text = response.content.decode('unicode-escape').replace('\n', '').replace('\r', '')
        pattern = re.compile('"pagehtml":(.*)}}')
        return pattern.findall(text)[0]
        # text = text.replace(pattern.findall(text)[0], '').replace(',"pagehtml":','')
        # import json
        # # print(text)
        # jsn = json.loads(text, strict=False)
        # pprint.pprint(jsn)


def qyer_poi_detail():
     url = 'https://place.qyer.com/poi/V2UJYVFkBzJTZVI9/'
     with requests.session() as sess:
         response = sess.get(url)
         print(response.text)
content = {
    'play': '娱乐',
    'scenery': '景点'
}


def lvmama_parse_poi_list(url):
    with requests.session() as sess:
        response = sess.get(url)
        html = HTML(response.text)
        base_id_pattern = re.compile('base_id  :"(\d+)",')
        base_id = base_id_pattern.findall(response.text)[-1]
        print(base_id)
        # a_list = html.xpath('.//div[@id="viewspot_list"]/dl/dd/div[@class="title"]/a')
        # if not a_list:
        #     a_list = html.xpath('.//div[@id="play_list"]//dl//div[@class="item-info"]//strong/a')
        # if not a_list:
        #     a_list = html.xpath('.//div[@id="view_list"]//dl/dd//a')
        # for a in a_list:
        #     # urls = [url for url in urls if url.startswith('http://www.lvmama.com/lvyou') and not url.endswith('#dianping')]
        #     # for url in urls:
        #
        #     url = get_text_by_xpath(a, '@href')
        #     title = get_text_by_xpath(a, 'text()')
        #
        #     if url.startswith('http://www.lvmama.com/lvyou/poi'):
        #         print(url)
        #     else:
        #         # 'http://www.lvmama.com/lvyou/d-lasiweijiasi3719.html'
        #         lase_index = len(url) - url[::-1].index('/')
        #         for type in content.keys():
        #             temp_url = url[:lase_index - 1] + '/' + type + url[lase_index - 1:]
        #             print(temp_url)
        #             lvmama_parse_poi_list(temp_url)
        #             # yield Request(url=url[:lase_index - 1] + '/' + type + url[lase_index - 1:],  meta={'country': response.reqeust.meta.get('country'), 'type': type}, callback=self.parse_poi_list)


def lvmama_poi_detail(url):
    with requests.session() as sess:
        response = sess.get(url)
        html = HTML(response.text)
        item = LvmamaPoiDetailItem()
        item['raw'] = {'html': str(lzma.compress(response.content))}
        if 'sight' in url:
            item['head'] = get_text_by_xpath(html, './/span[@class="crumbs_nav"]/span//text()')
            item['title'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/h2[@class="title"]/text()')
            item['title_en'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/span[@class="title-eng"]/text()')
            item['vcomon'] = get_text_by_xpath(html, './/div[@class="vtop-name-box"]/i[@class="vcomon-icon"]/text()')
            # item['country'] = response.request.meta.get('country')
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

        # item['url'] = response.request.url
        return item

import json
def lvmama_get_view_list():
    url ='http://www.lvmama.com/lvyou/ajax/getNewViewList?page_num=3&dest_id=3571&base_id=12&request_uri=%2Flvyou%2Fscenery%2Fd-meiguo3571'
    with requests.session() as sess:
        response = sess.get(url)
        obj = json.loads(response.text)
        html = HTML(obj.get('data'))
        print(html.xpath('.//dl/dd/div[@class="title"]/a/text()'))

def lvmama_get_play_list():
    url ='http://www.lvmama.com/lvyou/poi/sight-182536.html'
    with requests.session() as sess:
        response = sess.get(url)
        obj = json.loads(response.text)
        html = HTML(obj.get('data').get('html'))
        print(html.xpath('.//dl//div[@class="item-info"]//strong/a/text()'))
        # print(html.xpath('.//dl/dd/div[@class="title"]/a/text()'))

def  haoqiao():
    from tools import get_cookie
    url ='https://www.haoqiao.com/hotellist?city=33&hq_language=zh-CN&page=10&checkin=2019-04-24&checkout=2019-04-25&room=1&adult=2&child=0&child_age=&citizenship=CN&token=&sequence=web_1587605108899_525987/hotellist?city=1618&hq_language=zh-CN&page=2&checkin=2019-04-24&checkout=2019-04-25&room=1&adult=2&child=0&child_age=&citizenship=CN&token=&sequence=web_1587605108899_525987&is_refresh=1&req_type=ajax&vt=&hash=&timestamp='
    with requests.Session() as sess:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "referer": "https://www.haoqiao.com/palmcove_c1618",
            'accept-language': 'zh-CN,zh;q=0.9',
            "x-requested-with": "XMLHttpRequest",
        }

        cookies = get_cookie("hq_language=zh-CN; currency=CNY; _hq_=744161054f7f2369f1b201da167cd14d; Hm_lvt_9607b4b82cc66a1db5a1d051a029df0c=1587603306; PHPSESSID=neq1c7gehf4sitagnirnlcoev2; Hm_lpvt_9607b4b82cc66a1db5a1d051a029df0c=1587605305; SERVERID=56f633227ef7f9c3a66f1cf235d11366|1587608992|1587608992; sea_arr=sea_arr=%7B%22checkin%22%3A%222019-04-24%22%2C%22checkout%22%3A%222019-04-25%22%2C%22room%22%3A%221%22%2C%22adult%22%3A%222%22%2C%22child%22%3A0%2C%22child_age%22%3A%22%22%2C%22citizenship%22%3A%22CN%22%7D; city=%E6%A3%95%E6%A6%88%E6%B9%BE; city_id=1618")
        cookies = None

        response = sess.get(url, headers=headers, cookies=cookies)
        # print(response.cookies)
        # return response.content.decode('unicode_escape')
        return json.loads(response.text)


def haoqiao_create_vt():
    import execjs
    js = execjs.compile(""" function js_encrypt(str, pwd) {
        var prand = "";
        for(var i=0; i<pwd.length; i++) {
            prand += pwd.charCodeAt(i).toString();
        }
        var sPos = Math.floor(prand.length / 5);
        var mult = parseInt(prand.charAt(sPos) + prand.charAt(sPos*2) + prand.charAt(sPos*3) + prand.charAt(sPos*4) + prand.charAt(sPos*5));
        var incr = Math.ceil(pwd.length / 2);
        var modu = Math.pow(2, 31) - 1;
        if(mult < 2) {
             
            return null;
        }
        var salt = Math.round(Math.random() * 1000000000) % 100000000;
        prand += salt;
        while(prand.length > 10) {
            prand = (parseInt(prand.substring(0, 10)) + parseInt(prand.substring(10, prand.length))).toString();
        }
        prand = (mult * prand + incr) % modu;
        var enc_chr = "";
        var enc_str = "";
        for(var i=0; i<str.length; i++) {
            enc_chr = parseInt(str.charCodeAt(i) ^ Math.floor((prand / modu) * 255));
            if(enc_chr < 16) {
                enc_str += "0" + enc_chr.toString(16);
            } else enc_str += enc_chr.toString(16);
            prand = (mult * prand + incr) % modu;
        }
        salt = salt.toString(16);
        while(salt.length < 8)salt = "0" + salt;
        enc_str += salt;
        return enc_str;
    }""")
    print(js.call("js_encrypt", "hq_1587607680211", "haoqiao"))

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "referer": "https://hotels.ctrip.com/international/cairo332",
       "origin": "https://hotels.ctrip.com",
        'accept-language': 'zh-CN,zh;q=0.9',
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie":"IntlVID=110106-b9ec9c1c-cc02-441b-a40b-1dfb3a70554e; ASP.NET_SessionSvc=MTAuNjEuMjIuMjQ0fDkwOTB8amlucWlhb3xkZWZhdWx0fDE1ODcwMzY2MzE1NjQ; _abtest_userid=044dd48e-2673-4858-8c15-d75c97da697f; magicid=BZyFeJreZzWD9qpamZkiWb0PCaizcJ3CefsWWrOPnqfBaLSQv4yIN4/TI76Mhhde; clientid=51482037310776938090; IntHotelCityID=splitsplitsplit2020-04-25split2020-04-26splitsplitsplit1split1split1; hoteluuid=16LXCtMgpNHdu7lS; hoteluuidkeys=mH8YctRQXeanEXOWfYGY5mY8dE4YgY0pec0EG1jU5WzYfYtpjznwaqImzjcY9Yk0jP4yQfjB8w5YtY7QrSMIn6vDcIqYFY3BIDOiSsyl1j5typhe0liMNjnNy1Y5YhHvoAv6SJb4whSjgBeAHiXtYmYHYOYZY4Lvtzes6YOFilcYMYtYmYHYPME1tKoDwTBilHRmTjOrGOY90JaXyMrdMYdfW6bvksxUSe7mYPOx0ax1ZYHmi31w6cjm1EFOJMTW64jfrPnJSziTfwlcv43R6ZjzbYkSjOrFUyhni01wkMRz9EtUjgzxtAx4XEAbE7fEcdWNOeTBw4PE9aj6FeUZiATYHOr8he6geo6xDcic7it1xsGWqpjGUe7DwcQK3ZwUTi0QRFbjQoepqEOXy1kvB1iDUE0syfbvG5KHBEoqKg3wXpiFdRQ9j7rQ7YD5JbMycrFMj4seQmjohKsdjM3wtUxHhxpgx3qxMSE46EmNEdnWD4eFMwk8EZ1j47eM0iG4YMBrNPEfMygmvLgizTEOfyDhvP7KnmWNhEtzjn1eLOx7hjmrNQEGZWlZeSTj95YA4j56x0mxXNxz8xTqEofEX7EN9WtDeh9wFOEqGjbceBfipOYfLr1Qe6lefSYTkENcwmBWAmi00KtGEhlEmNEUsWsZefBw01Ea3j8lePFicFY4hrm7esLekQE3TY8AEf3wnXW0niHYFYUmY0Pi7BihNimajMY0YGLEN7j5ajmzJ4Gj0OwLlyP1wNYUYlDRUPJQSjnQysGytoRghvqkEFOYU5RtFvSdRhGvDYHYNtRP1w35IUUxSfEzmjGUr38xlaE6PWODvqLyc6vGay9mWp9JmYNYGYgY8ZjH9wNav5g; _bfa=1.1587719422430.2snmdl.1.1587719422430.1587719422430.1.1; _bfs=1.1; __utma=13090024.31103386.1587719423.1587719423.1587719423.1; __utmc=13090024; __utmz=13090024.1587719423.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=13090024.2.10.1587719423; hotelhst=1261406863",
    }

def ctrip_test(page='1'):
    # url = 'http://admin:secret@local-domain.com:8000/path?checkIn=2020-04-24&checkOut=2020-04-25&destinationType=1&IsSuperiorCity=1&cityId=332&cityPY=cairo&rooms=1&childNum=1&roomQuantity=1&pageIndex=1&keyword=&keywordType=&LandmarkId=&districtId=&zone=&metrostation=&metroline=&price=&star=&equip=&brand=&group=&fea=&htype=&promotionf=&coupon=&a=&orderby=&ordertype=1&isAirport=0&hotelID=&priceSwitch=&lat=&lon=&clearHotelName=&InitPageLoad=F&disCountItemSelected=%5B%5D&lat_cityCenter=30.0444196&lon_cityCenter=31.2357116&searchByDisLenovoHotelId=0&TopSetHotelListFromUrl=&pageid=102102&eleven=f7d78bebfff7d6fe5b82154b286dd4444eb3ad84dac6aa7ea15db1554eb9b958_1852316488&hasMapLoaded=T&IsNeedHermesRefresh=F&preHotelIdList=2231787%2C2109790%2C2109679%2C2106131%2C2196344%2C2545704%2C2196512%2C2878585%2C9452706%2C3137029%2C3743348%2C2545706%2C6618723%2C2143879%2C2196013%2C1060994%2C11068785%2C2104472%2C2195450%2C3914159%2C2195451%2C14941311%2C3031199%2C2139856%2C3033302&IsPreloadAjax=T'
    # data = get_url_query(url)
    # pprint.pprint(data)
    url = "https://hotels.ctrip.com/international/tool/AjaxHotelList.aspx"

    data = {'checkIn': '2020-04-24',
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
    data = {'checkIn': '2020-04-24', 'checkOut': '2020-04-25', 'destinationType': '1', 'IsSuperiorCity': '1', 'cityId': '5443',
     'cityPY': 'narrandera', 'rooms': '1', 'childNum': '1', 'roomQuantity': '1', 'pageIndex': page, 'keyword': '',
     'keywordType': '', 'LandmarkId': '', 'districtId': '', 'zone': '', 'metrostation': '', 'metroline': '',
     'price': '', 'star': '', 'equip': '', 'brand': '', 'group': '', 'fea': '', 'htype': '', 'promotionf': '',
     'coupon': '', 'a': '', 'orderby': '2', 'ordertype': '1', 'isAirport': '0', 'hotelID': '', 'priceSwitch': '',
     'lat': '', 'lon': '', 'clearHotelName': '', 'InitPageLoad': 'F', 'disCountItemSelected': '[]',
     'lat_cityCenter': '30.0444196', 'lon_cityCenter': '31.2357116', 'searchByDisLenovoHotelId': '0',
     'TopSetHotelListFromUrl': '', 'pageid': '102102',
     'eleven': '76980900c485f24c274b23a3bc6199f495d9bf7bdff252729409f140086a0404_1852097478', 'hasMapLoaded': 'T',
     'IsNeedHermesRefresh': 'T', 'preHotelIdList': '', 'IsPreloadAjax': 'F'}
    cookies_str = "curPagePyramids=; checkInDateInfo=checkInDate=2020-04-24; hasViewedqCode=qCodeBtnUnfold=1; IntlVID=110106-fc197ec6-f3f1-4984-af03-8efd31b4c315; IntlVH=45584997=NDU1ODQ5OTc=&736267=NzM2MjY3; visitedMinPriceSubroomHistoryListInfo_2=visitedMinPriceSubroomHistoryList=%7B%222104476%22%3A478%2C%223914159%22%3A586%2C%2214941311%22%3A94%2C%2245584997%22%3A162%2C%22idKeyList%22%3A%5B%2214941311%22%2C%223914159%22%2C%222104476%22%2C%2245584997%22%5D%7D; userinfo=checkInMinDate=2020-04-24;currentPageIndex=1; _abtest_userid=fd4fd656-baec-4872-9817-4700f4cd5998; magicid=s3PairXrLrEkr+CMhN9S0KqeV5F7j+HUrS6U/DzEcf7BaLSQv4yIN4/TI76Mhhde; clientid=51482090210776652021; IntHotelCityID=splitsplitsplit2020-04-24split2020-04-25splitsplitsplit1split1split1; hoteluuid=16LXCtMgpNHdu7lS; MKT_CKID=1587629099132.nz26j.cb5i; MKT_Pagesource=PC; _ga=GA1.2.784265839.1587629093; _gid=GA1.2.1116243172.1587629099; _RSG=xtakgKIUZNCpgd.ugDbGu9; _RDG=28aaa3ccf0de7f27de0e6c746da11db494; _RGUID=c5e37925-2aba-4dfb-9e10-94dab8fa7ab3; ASP.NET_SessionSvc=MTAuMjUuNzIuMjV8OTA5MHxvdXlhbmd8ZGVmYXVsdHwxNTg3MDM1MTMwODIy; __utmc=13090024; IntlIOI=F; _HGUID=%03U%05SWYRUMR%01%02%01MT%04%06%02MY%05QPMYT%04%01%02X%06%01W%01%02S; fcerror=870755330; _zQdjfing=3a923a3165bb4ea0843165bbd5c086d5c0865fa4cc5fa4cc4ea084; __utma=13090024.784265839.1587629093.1587716060.1587716060.1; __utmz=13090024.1587716060.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); MKT_CKID_LMT=1587716064869; _RF1=101.95.169.14; hoteluuidkeys=3f4YkPKkHeQmEcUW3Y4YL3Yb0EAYQYLFeOqEBfjHtWlY4YnPjlbwfBvQfeTYXYcZj8XRp7vNhjMYoY0Lw1dYbNv6PegYhYc9vm3Yz8yH5j7LJzqeZcYGFjMpyaYZYk1vtfv6qJtTwNHjG5edoiMpY8YhYdY8Y5qvtbedgYa8iG4Y3YlY1YTYtNEH3K6twoFibsRTzjmr3TY1HJNTycrN4Y56WX1vaGxLOeTMYHhxf8xSBYd0ipLwOkjLfETLJ6gWDbjPrmLJNkiZFwhbvnSRFfjD8Y6Bj6rOFyp9ig8w9mRkFEagjm4x3NxSoEaUEMnE51WUae70wHhEmqjDGeqQi0AYB1rpOezDeP4x3diksi7GxOgWbZjPSeaPwQgKf3wh3i9HRoHjGmeDUEF5y6cvd8iPkELUyOAvzQKncEgMKGhwFLikMRHFjUrp1YTzJhzySrt7j4UetkjGhK48jMLwSdx1Sx40x6AxQ8Ec7EqoESoW15eOzwk1E0XjUSe0GibQYFnr6dEsZyapvtli6PEgPyn1vk9KF1W1bE06jsze5Dxpojqr8qEnoWX1elXjZAYpGjM0x3XxGTxSaxbXE9bENPEOFW8ZecHwGXEdDj58eDMigZY5pr3begqenbYotEODw1DWfSiDDKGkEAqE9OEhSWoSeXhwFhE5FjoOepsifSYZhr0qeN7eqHE0XYflES6wQSWSLilY5YU8Y3Gi4Zi4bibzjPYzYaFEpajzlj06JZgjh4wtUy7TwZYLY8hRFAJ7ljtBy47yGXRDoy18ykBvLkiomwZhJlkE0YQY1dRbtwTcImmxXtEPdjXQr80xXpEDTWlzvoOyF7v0Gy0HWc7JPYkY3ORA3JQ9jslyObytSRcbwLhW4DJN4v43YONRM7i7YsYtQjpgw4mv6M; __utmb=13090024.6.10.1587716060; _jzqco=%7C%7C%7C%7C%7C1.113527430.1587716064857.1587716981144.1587717796348.1587716981144.1587717796348.0.0.0.3.3; __zpspc=9.1.1587716064.1587717796.3%234%7C%7C%7C%7C%7C%23; appFloatCnt=3; _bfa=1.1587716059213.vuqgy.1.1587716059213.1587716059213.1.17; _bfs=1.17; _bfi=p1%3D102102%26p2%3D102102%26v1%3D17%26v2%3D16; hotelhst=1261406863"
    cookies = get_cookie(cookies_str)
    cookies = None

    proxy = {"https": "58.218.200.228:8596"}
    with requests.Session() as sess:
        res = sess.post(url, data=data, headers=headers, cookies=cookies, proxies=None)
        print(json.loads(res.text))

import threading

def main(th):
    for i in range(1, 10):
        print('线程{}-{}'.format(th, i))
        ctrip_test(str(i))


if __name__ == '__main__':
    threads = []
    for i in range(10):
        t = threading.Thread(target=main, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    # ctrip_test()
