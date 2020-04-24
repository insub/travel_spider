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
    catename = scrapy.Field()
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


class LvmamaPoiItem(MongoDBItem):
    collection = 'lvmamam_poi'
    raw = scrapy.Field()

# class LvmamaPoiItem(MongoDBItem):
#     collection = 'lvmamam_poi'
#     raw = scrapy.Field()

class LvmamaPoiDetailItem(MongoDBItem, MysqlItem):
    '''
    lvmama poi 详情
    '''
    collection = 'lvmamam_poi_detail'
    table = 'lvmamam_poi_detail'

    # raw 字段存入mongodb
    raw = scrapy.Field()

    country = scrapy.Field()
    head = scrapy.Field()  # 头
    title = scrapy.Field()  # 中文标题
    title_en = scrapy.Field()  # 英文标题
    vcomon = scrapy.Field()  # 景点类型

    active = scrapy.Field()  # 活动内容
    poi_detail = scrapy.Field()  # 景点导览
    poi_brief = scrapy.Field()  # 景点介绍
    address = scrapy.Field()  # 地　　址
    arrive_method = scrapy.Field()
    open_time = scrapy.Field()  # 开放时间
    playtime = scrapy.Field()  # 游玩时间
    website = scrapy.Field()  #官方网址
    traffic = scrapy.Field()  # 交通
    ticket = scrapy.Field()  # 门票说明
    phone = scrapy.Field()  # 联系电话：
    poi_tip_content = scrapy.Field()  # 小贴士
    url = scrapy.Field()
    website = scrapy.Field()  # 官方网址


class HaoqiaoItem(MysqlItem):
    table = 'haoqiao_hotel_list'
    title = scrapy.Field()
    title_en = scrapy.Field()
    city = scrapy.Field()
    city_id = scrapy.Field()
    url = scrapy.Field()


class HaoqiaoMDBItem(MongoDBItem):
    collection = 'haoqiao_hotel_list'
    raw = scrapy.Field()


class CtripHoteItem(MysqlItem):
    """:param
    携程酒店列表的条目
    """
    table = 'ctrip_hotel_list'

    title = scrapy.Field()
    title_en = scrapy.Field()
    city = scrapy.Field()
    city_id = scrapy.Field()
    url = scrapy.Field()


class CtripHotelMDBITem(MongoDBItem):
    collection = 'ctrip_hotel_list'
    raw = scrapy.Field()


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