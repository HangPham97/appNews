# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import os
import requests
import shutil
from urllib.parse import urlparse

from scrapy.exceptions import DropItem

from appNews.models import session, Article

from appNews import settings

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set([t.lid for t in session.query(Article).all()])

    def process_item(self, item, spider):
        if item['lid'] in self.ids_seen:
            spider.logger.info("Drop duplicate item: {}".format(item["lid"]))
            raise DropItem("Duplicate item found: {}".format(item["lid"]))
        else:
            self.ids_seen.add(item['lid'])
            return item
# class ImagePipeline(object):
#     def close_spider(self, spider):
#         session.close()
    
#     def process_item(self, item, spider):
#         #Clone cover
#         image_url = item.get('cover_origin')
#         new_image_url = self._clone_image(image_url)
#         item['cover'] = new_image_url

#         image_pattern = re.compile(r'')
#         content_image_urls = set(image_pattern.findall(item.get('content')))
#         for image_url in content_image_urls:
#             new_image_url = self._clone_image(image_url)
#             item['content'] = item['content'].replace(image_url, new_image_url)
#         return item

    # def _clone_image(self, image_url):
    #     url_path = urlparse(image_url).path
    #     url_path = url_path[1:]

    #     filename = url_path.replace('/','_').lower()
    #     file_path = f'{settings.MEDIA_DIR}/{filename}'
    #     new_image_url = f'https://{settings.MEDIA_DOMAIN}/images/{filename}'

    #     if not os.path.exists(file_path):
    #         r = requests.get(image_url, stream=True)
    #         if r.status_code != 200:
    #             raise DropItem(f'Can not download image: {image_url}')

    #         with open(file_path, 'wb') as f:
    #             r.raw.decode_content = True
    #             shutil.copyfileobj(r.raw, f)

    #     return new_image_url

class SQLPipeline(object):
    """Pipeline to save to SQL Database"""

    def close_spider(self, spider):
        session.close()
    
    def process_item(self, item, spider):
        article, is_created = self.__get_article(item)

        if not is_created:
            session.add(article)
            session.commit()

        return item

    def __get_article(self, item):
        article = session.query(Article).filter(
           Article.lid == item.get("lid")).first()
        
        if article:
           return article, True

        article = Article()

        # article.supercid = item.get('supercid')
        article.category = item.get('category')
        article.author = item.get('author')
        article.lid = item.get('lid')

        # article.sid = item.get('sid')
        article.sid_text = item.get('sid_text')     # FIXME: Remove
        article.url = item.get('url')

        article.title = item.get('title')
        article.post_time = item.get('post_time')
        # article.post_time_text = item.get('post_time_text')   # FIXME: Remove
        article.content = item.get('content')
        article.desc = item.get('desc')
        article.cover = item.get('cover')
        article.cover_origin = item.get('cover_origin')

        return article, False