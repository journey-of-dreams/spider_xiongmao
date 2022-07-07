# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicsItem(scrapy.Item):
    # define the fields for your item here like:
    detailUrl = scrapy.Field()  # 详情链接
    rating = scrapy.Field()  # 评分
    sort = scrapy.Field()  # 分类
    year = scrapy.Field()  # 年份
    imgSrc = scrapy.Field()  # 图片
    title = scrapy.Field()  # 标题
    intro = scrapy.Field()  # 介绍
    actor = scrapy.Field()  # 主演
    director = scrapy.Field()  # 导演
    newJi = scrapy.Field()  # 最新一集
    newDate = scrapy.Field()  # 更新时间
    linkLists = scrapy.Field()  # 视频链接列表
    total = scrapy.Field()  # 总集数

    pass