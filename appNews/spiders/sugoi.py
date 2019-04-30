from datetime import datetime

import scrapy
from scrapy.http.request import Request

from appNews.items import ArticleItem



class BikaeSpider(scrapy.Spider):
    name = 'sugoi'
    allowed_domains = ['sugoi.vn']
    start_urls = ['http://sugoi.vn']

    custom_settings = {
        'ITEM_PIPELINES': {
            'appNews.pipelines.DuplicatesPipeline': 100,
            'appNews.pipelines.SQLPipeline': 300,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.categories = [
            'am-thuc',
            'chia-se',
            'du-lich',
            'video-giai-tri',
            'hoc-tap',
            'tim-nha',
            'tin-tuc',
            'van-hoa-xa-hoi',
            'viec-lam'
        ]

    def close(self, spider):
        self.logger.info("Done")

    def start_requests(self):

        for category in self.categories:
            url = f'http://sugoi.vn/category/{category}/'

            yield Request(url, self.parse)

    def parse(self, response):
        for sel in response.xpath('//div[@class="td-ss-main-content"]/div[position()<11]'):
            item = ArticleItem()
            item['sid_text'] = 'sugoi.vn'
            url = sel.xpath('.//h3//@href').extract_first('').strip()
            item['url'] = url
            item['lid'] = url
            item['cover_origin'] = sel.xpath('./div[@class="td-module-thumb"]//@src').extract_first('').strip()
            item['desc'] = sel.xpath('.//div[@class="td-excerpt"]//text()').extract_first('').strip()
            item['category'] = response.xpath('.//div[@class="td-module-meta-info"]/a/text()').extract_first('').strip()
            item['author'] = response.xpath('.//span[@class="td-post-author-name"]/a/text()').extract_first('').strip()
            post_time = sel.xpath('.//span[@class="td-post-date"]//text()').extract_first('').strip()
            item['post_time'] = datetime.strptime(post_time, '%d/%m/%Y')
            request = scrapy.Request(url, callback=self.parse_data)
            request.meta['article'] = item
            yield request
        next_page = response.xpath('//div[@class="td-ss-main-content"]/div[last()]/a[last()]//@href')
        if next_page:
            url = next_page.extract_first().strip()
            yield scrapy.Request(url, callback=self.parse)

    def parse_data(self, response):
        item = response.meta['article'].copy()
        item['title'] = response.xpath('//h1[@class="entry-title"]//text()').extract_first('').strip()
        item['content'] = response.xpath('//div[@class="td-post-content"]').extract_first('').strip()
        return item