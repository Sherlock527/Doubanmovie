# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from ..items import ReviewItem


class DbreviewSpider(RedisCrawlSpider):
    name = 'dbreview'
    allowed_domains = ['douban.com']
    # Redis里有一个阻塞的列表queue，等待塞数据，不用给start_urls，spider会从中读取urls
    # start_urls = ['https://movie.douban.com/subject/3878007/comments?start=0&limit=20']

    redis_key = 'dbreview:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        reviews = response.xpath('//div[@class="comment-item"]//span[@class="short"]/text()').extract()
        for review in reviews:
            item = ReviewItem()
            item['review'] = review.strip()
            yield item
