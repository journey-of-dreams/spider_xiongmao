import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse
from xiongmao.items import ComicsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
import re
import requests


class YinghuaSpider(CrawlSpider):
    name = 'yinghua'
    allowed_domains = ['www.dmh8.com']

    conn = Redis(host='127.0.0.1', port=6379)
    count = 0
    def start_requests(self):
        try:
            for i in range(1, 10000):
                yield Request(url=f'http://www.dmh8.com/view/{i}.html', callback=self.parse_item)
        except Exception as e:
            print("数据爬取完毕")

    # start_urls = ['http://www.dmh8.com']
    #
    # link = LinkExtractor(allow=r'/view/\d+.html')
    # rules = (
    #     Rule(link, callback='parse_item', follow=True),
    # )

    def parse_item(self, response: HtmlResponse):
        self.count += 1
        print(f"共计{str(self.count)}部动漫")
        d1 = response.xpath('//div[@id="playlist1"]/ul/li')
        d2 = response.xpath('//div[@id="playlist2"]/ul/li')
        d3 = response.xpath('//div[@id="playlist3"]/ul/li')
        detail_items = max(d1, d2, d3, key=len)
        comics_item = ComicsItem()
        comics_item["total"] = len(detail_items)
        comics_item["title"] = response.xpath('//h1[@class="title"]/text()').extract_first()
        comics_item["rating"] = response.xpath('//div[@id="rating"]/span[@class="branch"]/text()').extract_first()
        time_date = response.xpath(
            ('//p[@class="data hidden-sm"]//span[@class="text-red"]/text()')).extract_first().split("/")
        comics_item["newJi"] = time_date[0]
        comics_item["newDate"] = time_date[1]
        comics_item["linkLists"] = []
        try:
            comics_item["intro"] = response.xpath(
                '//span[@class="data" and @style]/p/span/text() | //span[@class="data" and @style]/p/text() | //span[@class="data" and @style]/text() | //span[@class="data" and @style]/span/text()').extract_first().strip().replace(
                u'\u3000', u'').replace(u'\xa0', u'')
        except Exception as e:
            print(response.url)
            print(e)

        comics_item["imgSrc"] = response.xpath(
            '//div[@class="myui-content__thumb"]//img/@data-original').extract_first()
        detail_content = response.xpath('//div[@class="myui-content__detail"]').extract_first()
        sort = re.compile(r'分类：</span><a.*?>(.*?)</a>', re.S)
        year = re.compile(r'年份：</span><a.*?>(.*?)</a>', re.S)
        comics_item["sort"] = re.findall(sort, detail_content)[0]
        comics_item["year"] = re.findall(year, detail_content)[0].strip()
        # try:
        #     if self.link_list:
        #         self.link_list.clear()
        # except Exception as e:
        #     self.link_list = []

        for detail_item in detail_items:
            detail_url = detail_item.xpath('./a/@href').extract_first()
            # 每一集的详情页链接
            url = response.urljoin(detail_url)
            # 将详情页的url存入redis的set中
            ex = self.conn.sadd('urls', url)
            if ex == 1:
                yield Request(url=url, callback=self.parse_detail,
                              cb_kwargs={'item': comics_item})
            else:
                # print('数据还没有更新，暂无新数据可爬取！')
                pass

    def parse_detail(self, response: HtmlResponse, **kwargs):
        comics_item = kwargs['item']
        print(comics_item)
        bb = re.compile(r'vod_data".*"url":"(.*?)"', re.S)
        link = re.findall(bb, response.text)[0].replace('\\', '')
        ji = response.xpath('//a[@class="btn btn-warm"]/text()').extract_first()
        # self.link_list.append({"ji": ji, "link": link})
        # comics_item["linkLists"] = self.link_list
        comics_item["linkLists"].append({"ji": ji, "link": link})
        if len(comics_item["linkLists"]) == comics_item["total"]:
            yield comics_item
