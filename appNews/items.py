# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
    
    lid = scrapy.Field()                # String: load_id or link_id: id for article
    # supercid = scrapy.Field()           # Number: super_category_id
    # cid = scrapy.Field()                # Number: category_id

    # sid = scrapy.Field()                # Number: source_id
    sid_text = scrapy.Field()          

    url = scrapy.Field()                # String: original post url

    title = scrapy.Field()              # String
    post_time = scrapy.Field()          # Number
    category = scrapy.Field()
    author = scrapy.Field()
    # post_time_text = scrapy.Field()     

    desc = scrapy.Field()               # String
    cover = scrapy.Field()              # String: generate in ImagePipeline
    cover_origin = scrapy.Field()       # String

    content = scrapy.Field()            # String
    pass
