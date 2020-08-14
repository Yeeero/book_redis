import logging

import scrapy

logger = logging.getLogger(__name__)


class CrawlJdBookSpider(scrapy.Spider):
    name = 'crawl_book'
    allowed_domains = ['book.jd.com/booksort.html']
    start_urls = ['https://book.jd.com/booksort.html/']

    def parse(self, response):
        '''
            爬取京东书籍类
        :param response:
        :return:
        '''
        print('-----start crawl-----')
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            dt_name = dt.xpath(".//text()").get()
            em_list = dt.xpath(".//following-sibling::dd[1]/em")
            item[dt_name] = [{em.xpath(".//text()").get(): response.urljoin(em.xpath(".//@href").get())} for em in
                             em_list]
            # print(item)
            logger.warning(item)
            yield item
            # for em in em_list:
            #     href = em.xpath(".//@href").get()
            #     href = response.urljoin(href)
            #     if item.get(dt_name):
            #         item[dt_name].append({em.xpath(".//text()").get(): href})
            #     else:
            #         item[dt_name] = [{em.xpath(".//text()").get(): href}]
        # yield scrapy.Request(url=href, callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta['item']
        yield item
