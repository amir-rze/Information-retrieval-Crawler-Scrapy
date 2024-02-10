import json
import scrapy
# from crawler.spiders.newsDetail import NewsDetail
import requests
from crawler.items import CrawlerItem
from datetime import datetime as dt
from crawler.utils import get_random_agent
import sys
import datetime


def remove_whitespace_from_price(price):
    if price is not None:
        splited = price.split(' ')
        price = splited[0]
        return price
    else:
        return 'null'


class Phones(scrapy.Spider):
    name = 'phones'
    base_url = "https://emalls.ir"
    page_number = 2
    pagination_url = "https://emalls.ir/%D9%85%D8%AD%D8%B5%D9%88%D9%84%D8%A7%D8%AA~Category~39~b~Samsung~page~"
    has_page = True
    data = []
    start_urls = [
        'https://emalls.ir/%D9%85%D8%AD%D8%B5%D9%88%D9%84%D8%A7%D8%AA~Category~39~b~Samsung'
    ]

    def parse(self, response):
        phones_list = response.css('.item')
        if len(phones_list) > 0:
            for phone in phones_list:
                href = phone.css('::attr(href)').extract_first()
                detail = self.base_url + href
                yield response.follow(detail, callback=self.parse_detail)
        else:
            self.has_page = False  # the site doesn't have another page

        next_page = self.pagination_url + str(self.page_number)
        if self.has_page:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        items = CrawlerItem()
        name = response.css('.hidemore::text').extract_first()
        title = response.css('.hidemore>span::text').extract_first()
        max_price = remove_whitespace_from_price(response.css('span[style="color: #AF0303;"]::text').extract_first())
        min_price = remove_whitespace_from_price(response.css('span[style="color: #1AA603;"]::text').extract_first())
        link = None
        shops = response.css('.shop-price')
        for shop in shops:
            price = shop.css('::text').extract_first()
            if price == min_price:
                link = shop.css('::attr(href)').extract_first()
                break
        items['name'] = name
        items['title'] = title
        items['min_price'] = min_price
        items['max_price'] = max_price
        items['link'] = link

        dic = {
            'name': name,
            'title': title,
            'max_price': max_price,
            'min_price': min_price,
            'link': link
        }
        # try:
        #     with open('items.json') as f:
        #         data = json.load(f)
        #         f.close()
        # except:
        #     data = []
        # data.append(dic)
        with open("items.json", 'a', encoding='utf-8') as f:
            # json.dump(dic, f, ensure_ascii=False)
            f.write(f"{str(dic)}\n")

        f.close()
        yield items



