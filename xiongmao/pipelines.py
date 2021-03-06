# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy.crawler import Crawler
from redis import Redis


class MongoDBPipeline(object):
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        host = crawler.settings['MONGO_HOST']
        port = crawler.settings['MONGO_PORT']
        return cls(host, port)

    def __init__(self, host, port):
        print("初始化是佛触发")
        self.conn = Redis(host='127.0.0.1', port=6379)
        client = pymongo.MongoClient(host, port)
        db = client['xiongmao']
        self.Yinghua_lists = db['Yinghua_lists']
        # self.yinghua_data = []

    def close_spider(self, spider):
        # if len(self.yinghua_data) > 0:
        #     self.insert_item(self.Yinghua_lists, self.yinghua_data)
        #     self.yinghua_data.clear()
        pass

    def process_item(self, item, spider):
        print("_____________________________________________________-")
        if spider.name == 'yinghua':
            # self.yinghua_data.append(dict(item))
            # if len(self.yinghua_data) == 1:
            ex = self.conn.sadd('title', item['title'])
            if ex == 1:
                self.insert_item(self.Yinghua_lists, item)
            else:
                self.update_item(self.Yinghua_lists, item)
                print("更新一条")
        # 将item交给下一个管道类，推荐每一个process_item都return item
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            pass

    @staticmethod
    def update_item(collection, item):
        try:
            collection.update_one({"title": item['title']}, {
                "$set": {"total": item['total'], "rating": item['rating'], "newJi": item['newJi'],
                         "newDate": item['newDate']},
                "$addToSet": {"linkLists": {
                    "$each": item['linkLists']}}})
        except DuplicateKeyError:
            pass
