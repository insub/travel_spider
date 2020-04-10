# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import pymysql
from urllib.parse import quote_plus

from travel_spider.items import *
from travel_spider.utils import *
from travel_spider.settings import *


class TravelSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class TextPipeline(object):

    def open_spider(self, spider):
        self.spider = spider

    def process_item(self, item, spider):
        if isinstance(item, TextItem):
            write_error_log(spider, item)

    def close_spider(self, spider):
        pass


class MongoPipline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_user, mongo_password):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGO_URI'),
                   crawler.settings.get('MONGO_DB'),
                   crawler.settings.get('MONGO_USER'),
                   crawler.settings.get('MONGO_PASSWORD')
                   )

    def open_spider(self, spider):
        uri = "mongodb://%s:%s@%s/?authSource=%s&authMechanism=SCRAM-SHA-1" % (quote_plus(self.mongo_user), quote_plus(self.mongo_password), self.mongo_uri, self.mongo_db)
        # client = MongoClient(uri)
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[self.mongo_db]


    def process_item(self, item, spider):
        if isinstance(item, MongoDBItem):
            name = item.collection
            self.db[name].insert(item['raw'])
            return item

    def close_spider(self, spider):
        self.client.close()


class BookingImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, PhotoItem):
            yield scrapy.Request(url=item["image_url"], meta={'image_type': item['image_type']})

    def item_completed(self, results, item, info):
        # TODO 下载失败情况
        return item

    def file_path(self, request, response=None, info=None):
        """
        设置图片路径
        url 示例：'https://ac-q.static.booking.cn/images/hotel/max1024x768/226/226778927.jpg'
        """
        format_url = request.url.split('?')[0]
        file_name = "/".join(format_url.split('/')[-3:])
        folder = request.meta['image_type']
        return '{}/{}'.format(folder, file_name)


class MySQLPipeline(object):
    def __init__(self, host=MYSQL_URL, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE, charset='utf8'):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._charset = charset
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MYSQL_URL'),
                   crawler.settings.get('MYSQL_PORT'),
                   crawler.settings.get('MYSQL_USER'),
                   crawler.settings.get('MYSQL_PASSWORD'),
                   crawler.settings.get('MYSQL_DATABASE')
                   )

    def open_spider(self, spider):
        if self.conn is None:
            self.conn = pymysql.connect(host=self._host, port=self._port, database=self._database, user=self._user,
                                        password=self._password, charset=self._charset)
        elif isinstance(self.conn, type(pymysql.Connection)):
            self.conn.open()
        self.cursor = self.conn.cursor();

    def process_item(self, item, spider):
        if isinstance(item, MysqlItem):
            data = dict(item)
            if isinstance(item, MongoDBItem):
                del data['raw']
            keys = ', '.join(data.keys())
            values = ', '.join(['"%s"'] * len(data))
            sql = 'insert into %s (%s) values(%s)' % (item.table, keys, values)
            sql = sql % (tuple([str(value).replace('"', "'") for value in data.values()]))
            # with self.conn.cursor() as cursor:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql)
            self.conn.commit()
        return item

    def close_spider(self, spider):
        if self.conn is None:
            pass
        elif isinstance(self.conn, type(pymysql.Connection)):
            self.conn.close()

