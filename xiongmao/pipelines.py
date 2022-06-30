# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy.crawler import Crawler


class MongoDBPipeline(object):
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        host = crawler.settings['MONGO_HOST']
        port = crawler.settings['MONGO_PORT']
        return cls(host, port)

    def __init__(self, host, port):
        client = pymongo.MongoClient(host, port)
        db = client['xiongmao']
        self.Yinghua_lists = db['Yinghua_lists']

        self.yinghua_data = []

    # def close_spider(self, spider):
    #     if len(self.data) > 0:
    #         self._write_to_db()
    #     self.conn.close()
    #     pass

    def process_item(self, item, spider):
        if spider.name == 'yinghua':
            self.yinghua_data.append(dict(item))
            if len(self.yinghua_data) == 100:
                self.insert_item(self.Yinghua_lists, self.yinghua_data)
                self.yinghua_data.clear()
        # 将item交给下一个管道类，推荐每一个process_item都return item
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert_many(dict(item))
        except DuplicateKeyError:
            pass
