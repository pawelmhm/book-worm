# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader


class BookWormItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    djvu_url = scrapy.Field()
    year_url = scrapy.Field()

class BookWormItemLoader(ItemLoader):
    default_item_class = BookWormItem
