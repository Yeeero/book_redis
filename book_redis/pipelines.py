# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime


class BookRedisPipeline:
    def process_item(self, item, spider):
        print('*****pipeline*****')
        item['crawled'] = datetime.utcnow()  # 爬取的时间
        item['spider'] = spider.name  # 爬取的项目
        return item
