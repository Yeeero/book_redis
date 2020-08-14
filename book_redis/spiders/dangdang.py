from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider
import scrapy
from copy import deepcopy

'''
    爬取当当网所有书籍类商品的详细信息
'''


class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['book.dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = 'dangdang:start_urls'

    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(DangdangSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 大分类
        div_list = response.xpath("//div[@class='con flq_body']/div")
        for div in div_list:
            item = {}
            item['b_cate'] = div.xpath(".//dl/dt//text()").extract()
            # print(item)
            item['b_cate'] = [i.strip() for i in item['b_cate'] if len(i.strip()) > 0]

            # 中间分类分组
            dl_list = div.xpath(".//div//dl[@class='inner_dl']")
            for dl in div_list:
                item['m_cate'] = dl.xpath(".//dt//text()").get().strip()
                # 小分类分组
                a_list = dl.xpath(".//dd/a")
                for a in a_list:
                    item['s_href'] = a.xpath(".//@href").get()
                    item['s_cate'] = a.xpath(".//text()").get().strip()
                    if item['s_href'] is not None:
                        # yield scrapy.Request(item['s_href'], callback=self.parse_book_list, meta={'item': item})
                        yield scrapy.Request(url=item['s_href'], callback=self.parse_book_list, meta={"item": deepcopy(item)})

    def parse_book_list(self, response):
        print('----------parse_book_list------')
        item = response.meta['item']
        li_list = response.xpath("//ul[@class='bigimg']/li")
        if li_list == []:
            li_list = response.xpath("//ul/li")
        for li in li_list:
            item['book_img'] = li.xpath(".//div[@class='pic']/img/@src").get()
            if item['book_img'] == "img/model/guan/url_one.png":
                item['book_img'] == li.xpath(".//a[@class='pic']/img/@data-original").get()
            item['book_name'] = li.xpath(".//p[@class='name']/a/@title").get()
            item['book_desc'] = li.xpath(".//p[@class='detail']/text()").get()
            item['book_price'] = li.xpath(".//span[@class='search_now_price']/text()").get()
            item['book_author'] = li.xpath(".//p[@class='search_book_author']/span[1]/a/text()").get()
            item['book_publish_date'] = li.xpath(".//p[@class='search_book_author']/span[2]/text()").get()
            item['book_press'] = li.xpath(".//p[@class='search_book_author']/span[e]/a/text()").get()
            # print(item)
            yield item
            break
        # next page
        # next_url = response.xpath("//li[@class='next']/a/@href").get()
        # if next_url is not None:
        #     next_url = response.urljoin(next_url)
            # yield scrapy.Request(url=next_url, callback=self.parse_book_list, meta={'item': item})    # 回调下一页


# if __name__ == '__main__':
#     d = DangdangSpider()