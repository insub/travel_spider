# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TravelSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MysqlItem(scrapy.Item):
    table = ""


class MongoDBItem(scrapy.Item):
    collection = ""


class PoiItem(MongoDBItem):
    '''
    POI列表
    '''
    collection = 'poi'
    # raw 字段存入mongodb
    raw = scrapy.Field()


class PoiDetailItem(MongoDBItem, MysqlItem):
    '''
    poi 详情
    '''
    collection = 'poi_detail'
    table = 'poi_detail'

    # raw 字段存入mongodb
    raw = scrapy.Field()

    id = scrapy.Field()
    head = scrapy.Field()
    title = scrapy.Field()
    title_en = scrapy.Field()
    rank = scrapy.Field()
    poi_detail = scrapy.Field()
    poi_tips = scrapy.Field()
    address = scrapy.Field()
    arrive_method = scrapy.Field()
    open_time = scrapy.Field()
    ticket = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    poi_tip_content = scrapy.Field()
    url = scrapy.Field()


class PhotoItem(scrapy.Item):
    """
    图片item
    pic_type:图片类型
    image_url: 图片地址
    """
    table = 'photo_visited'
    image_type = scrapy.Field()
    image_url = scrapy.Field()


class DFItem(scrapy.Item):
    df = scrapy.Field()
    columns = {}
    columns_name = [a for a in columns.keys()]

    def __init__(self):
        super(DFItem, self).__init__()
        # self["stock_code"] = ''

    def clean(self):
        pass

    def validate(self):
        pass


class TextItem(scrapy.Item):
    pass


class ErrorRequestItem(TextItem):
    '''
    请求错误的 request
    '''
    table = collection = "error_requests"
    spider_name = scrapy.Field()
    url = scrapy.Field()
    #错误信息，最大长度为500
    msg = scrapy.Field()