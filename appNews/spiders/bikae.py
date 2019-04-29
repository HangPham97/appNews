import json
# import time
from datetime import datetime

import scrapy
from scrapy.http.request import Request

from appNews.items import ArticleItem



class BikaeSpider(scrapy.Spider):
    name = 'bikae'
    allowed_domains = ['bikae.net']
    start_urls = ['https://bikae.net/']

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'appNews.pipelines.DuplicatesPipeline': 100,
            # 'appNews.pipelines.ImagePipeline': 200,
            'appNews.pipelines.SQLPipeline': 300,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.categories = [
            'my-pham-lam-dep',
            'am-thuc-mua-sam',
            'di-lai-du-lich',
            'cham-soc-suc-khoe',
            'me-va-be',
            'doi-song',
        ]

    def close(self, spider):
        self.logger.info("Done")

    def start_requests(self):

        for category in self.categories:
            url = f'https://bikae.net/category/{category}/'

            yield Request(url, self.parse)

    def parse(self, response):
        for sel in response.xpath('//article'):
            item = ArticleItem()
            item['sid_text'] = 'bikae.net'
            url = sel.xpath('.//h1[@class="entry-title"]//@href').extract_first('').strip()
            item['url'] = url
            item['lid'] = url
            item['title'] = sel.xpath('.//h1[@class="entry-title"]//text()').extract_first('').strip()
            item['cover_origin'] = sel.xpath('.//div[contains(@class,"toppage-post-feature-img")]//@src').extract_first('').strip()
            item['desc'] = sel.xpath('.//div[@class="toppage-post-excerpt"]/div/text()[1]').extract_first('').strip()
            item['category'] = response.xpath('//strong[@class="breadcrumb_last"]').extract_first('').strip()
            item['author'] = response.xpath('.//span[@class="byline"]').extract_first('').strip()
            post_time_full = sel.xpath('.//time[1]/@datetime').extract_first('').strip()
            post_time = post_time_full[:10]
            item['post_time'] = datetime.strptime(post_time, '%Y-%m-%d')
            request = scrapy.Request(url, callback=self.parse_data)
            request.meta['article'] = item
            yield request
        next_page = response.xpath('//div[@class="nav-next"]//@href')
        if next_page:
            yield scrapy.Request(url, callback=self.parse)

    def parse_data(self, response):
        item = response.meta['article'].copy()
        item['content'] = response.xpath('//article').extract_first('').strip()
        return item