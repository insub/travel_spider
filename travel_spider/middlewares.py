# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import requests
from scrapy import signals
from scrapy.http import HtmlResponse

from travel_spider.spiders.haoqiao_spider import HaoqiaoSpider
from travel_spider.spiders.ctrip_spider import CtripSpider

class TravelSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class TravelSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "referer": "https://www.haoqiao.com/palmcove_c1618",
            'accept-language': 'zh-CN,zh;q=0.9',
            "x-requested-with": "XMLHttpRequest",
        }

        if isinstance(spider, HaoqiaoSpider):

            with requests.Session() as sess:
                response = sess.get(request.url, headers=headers)
                return HtmlResponse(url=request.url, request=request, body=response.content)
        elif isinstance(spider, CtripSpider):
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                "referer": "https://hotels.ctrip.com/international/cairo332",
                "origin": "https://hotels.ctrip.com",
                'accept-language': 'zh-CN,zh;q=0.9',
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "cookie": "IntlVID=110106-43a0f2d8-5fa2-4675-a4f2-363662277b43; ASP.NET_SessionSvc=MTAuMjUuMTY3LjQ4fDkwOTB8b3V5YW5nfGRlZmF1bHR8MTU4NzAzNTgyMjY3OA; _abtest_userid=fd4fd656-baec-4872-9817-4700f4cd5998; magicid=s3PairXrLrEkr+CMhN9S0KqeV5F7j+HUrS6U/DzEcf7BaLSQv4yIN4/TI76Mhhde; clientid=51482090210776652021; IntHotelCityID=splitsplitsplit2020-04-24split2020-04-25splitsplitsplit1split1split1; _bfa=1.1587629092942.355wwh.1.1587629092942.1587629092942.1.1; _bfs=1.1; hoteluuid=16LXCtMgpNHdu7lS; hoteluuidkeys=OpHy5tYcDe8sJX8WXYOYdSYgDEgYOYf1e9PEn4j1tW1Y6YzZjZpi5zeGNybYoY5dynGwL8I9tW5Y0YS1RAaRZdvlpj5YDYTOvpsYfbyAOjQ1vfhe6zeqgjhayfYzYZGvTOvA3YlkwP9jgXeF5iZ5Y9YTYzYMYS9vnteQ6YMpiHsYHY5YaYlYNaEO8KLtwtai15RSpj4rmTYThJ0pyNrS4YM7W1HvZSxz4e3HYfzxpHxNzYpniAqwmOjtOEFSJ1LWpHj1rDzJfliGLwL0vbtRlHjFHYsDjZrX6yHhil7wmgROXESDj1FxOdxXMEsUE3HEzaWbDeTnw5SEpojt8eaAiZQYsQr8pekaedAxXziSdiM4xAnWNSj60ebOwGqKo5wT3iscRB6jdgesnEb6yBfvqPiHgEkgyGmv1sKktEt0Kk8wP7idSRMkjNrSUYTQJQSylr6ZjpteTAjmfKLqjBhw91xDqxLsxZNxDfEXgE6oEF7WBheMZwPNEqUjBceD9i1LYSsrHNEDdyTZvPki6LEspygNvm8KDmWzLEsUjUTeQqxtnjsr7LENmWGpebgjzNYLdjN1xbXxs6xpAxsaEAHEZpEp3WbseNAwdzElAjBHeFUiT6YQdrNUe1te9dYO6EtmwSaWO6iddKSZEPhEl8EgQWtoe7gw5FEmlj4nebcio7YThraZes5eDAEUZYQPEn5wPZWlhi8YfYs9YHSiM4iSmidzjpYSYdFEa7jUOjlbJdDjbBwOgy46w4Y1Ym1RkMJzOjphylGw4nYhmv3OWUBvGQiN8Rptyf9YfYcY3URUOwkoIDDxGSESqjM5rL6xOFEfZWhbv1MyAGvpZy93WzaJzYtYoDR59JPSjZTyclwSHYZ3vmlWoavM3YT4voMElOYlYGYkPjOPwMUvNH; __utma=13090024.784265839.1587629093.1587629093.1587629093.1; __utmc=13090024; __utmz=13090024.1587629093.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=13090024.2.10.1587629093; MKT_CKID=1587629099132.nz26j.cb5i; MKT_CKID_LMT=1587629099133; __zpspc=9.1.1587629099.1587629099.1%234%7C%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.463871537.1587629099150.1587629099150.1587629099150.1587629099150.1587629099150.0.0.0.1.1; MKT_Pagesource=PC; appFloatCnt=1; _ga=GA1.2.784265839.1587629093; _gid=GA1.2.1116243172.1587629099; _gat=1; hotelhst=1261406863; _RF1=101.95.169.14; _RSG=xtakgKIUZNCpgd.ugDbGu9; _RDG=28aaa3ccf0de7f27de0e6c746da11db494; _RGUID=c5e37925-2aba-4dfb-9e10-94dab8fa7ab3; IntlIOI=F; _bfi=p1%3D102102%26p2%3D0%26v1%3D1%26v2%3D0"
            }
            with requests.Session() as sess:
                response = sess.post(request.url, headers=headers, data=request.meta['data'])
                return HtmlResponse(url=request.url, request=request, body=response.content)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
