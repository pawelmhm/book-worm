# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.loader.processors import TakeFirst, Join


class BookWormItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    djvu_url = scrapy.Field()
    year_url = scrapy.Field()
    content_id = scrapy.Field()
    file_path = scrapy.Field()
    text = scrapy.Field()
    crawl_id = scrapy.Field()


class BookWormItemLoader(ItemLoader):
    default_item_class = BookWormItem
    content_id_out = TakeFirst()
    djvu_url_out = TakeFirst()
    title_out = TakeFirst()
    file_path_out = TakeFirst()
    text_out = Join()

