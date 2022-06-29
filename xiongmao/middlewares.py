# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = 'history=%5B%7B%22name%22%3A%22%E7%A5%9E%E5%8D%B0%E7%8E%8B%E5%BA%A72022%22%2C%22pic%22%3A%22http%3A%2F%2Fsakura.xonlines.com%2Fupload%2Fvod%2F20220428-1%2Fed95376215b90b0b7cc6bfd29b762664.jpg%22%2C%22link%22%3A%22%2Fplayer%2F8783-0-0.html%22%2C%22part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%5D; PHPSESSID=0ocotmi1td6cqh7ubcedvc6hm0; Hm_lvt_ea6972a9380e5a8a6607cc4c62409955=1655188017,1655278597; Hm_lpvt_ea6972a9380e5a8a6607cc4c62409955=1655280252'
    cookies_dict = {}
    for item in cookies_str.split(";"):
        key, value = item.split("=", maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict

COOKIES_DICT = get_cookies_dict()
class XiongmaoSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
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


class XiongmaoDownloaderMiddleware:
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
        request.cookies = COOKIES_DICT
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response
    # 拦截异常的请求
    def process_exception(self, request, exception, spider):
        # 随机的代理ip
        # if request.url.split(":")[0] == 'http':
        #     request.meta['proxy'] = 'http://'+random.choice(self.PROXY_http)
        # else:
        #     request.meta['proxy'] = 'https://'+random.choice(self.PROXY_https)
        # request.meta['proxy'] = "http://ip:port"
        #将修正后的请求重新发送
        # return request


        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
