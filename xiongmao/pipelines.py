# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from scrapy.crawler import Crawler


class DbPipeline:
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        host = crawler.settings['DB_HOST']
        port = crawler.settings['DB_PORT']
        username = crawler.settings['DB_USER']
        password = crawler.settings['DB_PASS']
        database = crawler.settings['DB_NAME']
        return cls(host, port, username, password, database)

    def __init__(self, host, port, username, password, database):
        self.conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database,
                                    charset='utf8mb4', autocommit=True)
        self.cursor = self.conn.cursor()
        try:
            sql = """CREATE TABLE IF NOT EXISTS jan_list (
                                 id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                 title VARCHAR(150) COMMENT '标题',
                                 detailUrl VARCHAR(1000) COMMENT '详情链接',
                                 imgSrc VARCHAR(1000) COMMENT '图片链接',
                                 rating CHAR(10) COMMENT '评分',
                                 year INT(4) COMMENT '年份',
                                 newJi VARCHAR(50) COMMENT '最新一集',
                                 actor VARCHAR(5000) COMMENT '主演',
                                 create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                 update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  COMMENT '更新时间')"""
            self.cursor.execute(sql)
        except Exception as e:
            print("表格建立失败")
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_db()
        self.conn.close()
        pass

    def process_item(self, item, spider):
        # 字典通过get()拿值可以指定默认值，不至于拿不到时直接报错
        title = item.get("title", "")
        rating = item.get("rating", "")
        year = item.get("year", "")
        detailUrl = item.get("detailUrl", "")
        newJi = item.get("newJi", "")
        actor = item.get("actor", "")
        imgSrc = item.get("imgSrc", "")
        # 改成批量处理
        self.data.append((title, rating, year, detailUrl, newJi,actor, imgSrc))
        if len(self.data) == 100:
            self._write_to_db()
            self.data.clear()
        # 将item交给下一个管道类，推荐每一个process_item都return item
        return item

    def _write_to_db(self):
        try:
            print(self.data[0])
            self.cursor.executemany(
                f'''insert into jan_list(title,rating,year,detailUrl,newJi,actor,imgSrc)
                 values(%s,%s,%s,%s,%s,%s,%s)''', self.data
            )
            print("插入语句成功")
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
