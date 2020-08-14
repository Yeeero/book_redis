# -*- coding = utf-8 -*-
# @Time :
# @ Author : Yeeero
# @File : test1.by
# @Software : PyCharm
import requests
from lxml import etree


def main():
    url = 'https://www.amazon.cn/dp/B07S46RBYK'
    resp = requests.get(url)
    html = resp.content.decode('utf-8')
    parse_page(html)


def parse_page(html):
    response = etree.HTML(html)
    title = response.xpath("//h1[@id='title']/span[@id='productTitle']//text()")[0].split("（")[0]
    print(title)


if __name__ == '__main__':
    main()
