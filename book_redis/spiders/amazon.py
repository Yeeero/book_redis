import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/Kindle%E7%94%B5%E5%AD%90%E4%B9%A6/b?ie=UTF8&node=116169071&ref_=nav_topnav_giftcert']
    redis_key = "amazon:start_urls"

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # 匹配大分类小分类的url地址
        Rule(LinkExtractor(restrict_xpaths="//div[@id='departments']//ul/li"), follow=True),
        # 获取图书的url
        Rule(LinkExtractor(restrict_xpaths="//div[@id='mainResults']/ul/li//h2/.."), callback='parse_book_detail'),
        # 获取下一页的url
        Rule(LinkExtractor(restrict_xpaths="//div[@id='pagn']"), follow=True),
    )

    # def __init__(self, *args, **kwargs):
    #     '''Spider that reads urls from redis queue (amazon:start_urls).'''
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(AmazonSpider, self).__init__(*args, **kwargs)

    def parse_book_detail(self, response):
        print('------starting parse page ------', response.url)
        with open('test.html', 'w', encoding='utf-8') as fp:
            fp.write(response.body.decode('utf-8'))
        item = {}
        item['book_title'] = response.xpath("//h1[@id='title']/span[@id='productTitle']//text()").get()
        item['book_title'] = item['book_title'].split('（')[0] if item['book_title'] is not None else item['book_title']
        item['book_publish_date'] = response.xpath("//h1[@id='title']/span[last()]/text()").get()
        item['book_author'] = response.xpath("//spam[@class='author motFated']/a/text()").getall()
        item['book_img'] = response.xpath("//div[contains(@class,'books-img')]//img/@src").get()
        item['book_price'] = response.xpath("//span[@class='a-size-medium a-color-price']").get()
        item['book_cate'] = response.xpath("//div[@class='wayfinding-breadcrumbs_container']//li[last()]//a/text()").get()
        item['book_press'] = response.xpath("//b[text()='出版社']/../text()").get()
        item['book_desc'] = response.xpath("//noscript/div/text()").getall()
        item['book_desc'] = [i.strip() for i in item['book_desc'] if len(i.strip() > 0)]
        # item['press_desc'] = response.xpath("//div[@class='iframeContent']/b/text()").get()
        print(item)
