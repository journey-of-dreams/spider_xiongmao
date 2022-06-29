import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from xiongmao.items import ComicsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis


class YinghuaSpider(CrawlSpider):
    name = 'yinghua'
    allowed_domains = ['www.dmh8.com']

    conn = Redis(host='127.0.0.1', port=6379)
    def start_requests(self):
        yield Request(url=f'http://www.dmh8.com/view/5020.html', callback=self.parse_item)

    # start_urls = ['http://www.dmh8.com']
    #
    # link = LinkExtractor(allow=r'/view/\d+.html')
    # # rules元组中存放的是不同的规则解析器（封装好了某种解析规则)
    # rules = (
    #     # 规则解析器：可以将连接提取器提取到的所有连接表示的页面进行指定规则（回调函数）的解析
    #     Rule(link, callback='parse_item', follow=False),
    # )

    def parse_item(self, response: HtmlResponse):
        detail_items = response.xpath('//div[@id="playlist1"]/ul/li')
        comics_item = ComicsItem()
        comics_item["title"] = response.xpath('//h1[@class="title]').extract_first()
        comics_item["rating"] = response.xpath('//div[@id="rating"]/div[@class="branch"]').extract_first()
        time_date = response.xpath(('//div[@class="data hidden-sm"]/span[@class="text-red"]/text')).extract_first()

        for detail_item in detail_items:
            detail_url = detail_item.xpath('./a/@href').extract_first()
            url = response.urljoin(detail_url)
            # 将详情页的url存入redis的set中
            ex = self.conn.sadd('urls', url)
            if ex == 1:
                print('该url没有被爬取过，可以进行数据的爬取')
                yield Request(url=url, callback=self.parse_detail,cb_kwargs={'item':comics_item})
            else:
                print('数据还没有更新，暂无新数据可爬取！')

    def parse_detail(self, response: HtmlResponse,**kwargs):
        comics_item = kwargs['item']

        yield comics_item
