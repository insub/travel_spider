# -*- coding: utf-8 -*-

# Scrapy settings for travel_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'travel_spider'

SPIDER_MODULES = ['travel_spider.spiders']
NEWSPIDER_MODULE = 'travel_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'travel_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'travel_spider.middlewares.TravelSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'travel_spider.middlewares.TravelSpiderDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'travel_spider.pipelines.TravelSpiderPipeline': 300,
   'travel_spider.pipelines.MongoPipline': 300,
   'travel_spider.pipelines.MySQLPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



""" scrapy-redis配置 """
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

#
# SCHEDULER = 'scrapy_redis_bloomfilter.scheduler.Scheduler'
# DUPEFILTER_CLASS="scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis_bloomfilter.queue.PriorityQueue'


SCHEDULER_PERSIST = True
BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 30


SCHEDULER_FLUSH_ON_START = False
REDIS_START_URLS_AS_SET = False
REDIS_START_URLS_KEY = '%(name)s:start_urls'
# LOG_LEVEL = 'INFO'

'''解决redis 中request 跑完，爬虫仍然空跑的情况'''
MYEXT_ENABLED = True      # 开启扩展
IDLE_NUMBER = 60  # 配置允许的空闲时长，每5秒会增加一次IDLE_NUMBER，直到增加到12，程序才会close

# 在 EXTENSIONS 配置，激活扩展
EXTENSIONS = {
            'travel_spider.extensions.RedisSpiderSmartIdleClosedExensions': 500,
        }

'''log error request '''
FAIL_REQUEST_URLS_DIR = './'
ERROR_STATUS_CODE = 999
HTTPERROR_ALLOWED_CODES = [ERROR_STATUS_CODE]


# --------redis 配置信息----
''''测试环境'''''
# REDIS_HOST = '192.168.25.65'

''''生成环境'''''
REDIS_HOST = '192.168.25.58'
REDIS_PORT = 6379
# REDIS_PARAMS = {
#     'password': 'test,123456!'
# }

# --------mysql 配置信息-----------

''''测试环境'''''
# mysql_url = 'localhost'
''''生成环境'''''
MYSQL_URL = '192.168.25.100'
#
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'champion'
MYSQL_DATABASE = 'travel_spider'

PROXY_URL = 'http://192.168.124.22:5555/random'


# --------mongodb 配置信息----
# 用来存放raw data
MONGO_URI = '192.168.25.100'
MONGO_DB = 'travel_spider'
MONGO_USER = 'travel_spider'
MONGO_PASSWORD = 'root'

