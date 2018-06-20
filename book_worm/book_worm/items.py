# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.loader.processors import TakeFirst, Join, MapCompose


class BookWormItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    djvu_url = scrapy.Field()
    pdf_url = scrapy.Field()
    year_url = scrapy.Field()
    content_id = scrapy.Field()
    file_path = scrapy.Field()
    text = scrapy.Field()
    crawl_id = scrapy.Field()
    publication_name = scrapy.Field()
    publication_date_raw = scrapy.Field()
    publication_date = scrapy.Field()


class BookWormItemLoader(ItemLoader):
    default_item_class = BookWormItem
    default_output_processor = TakeFirst()
    text_out = Join()
    title_in = MapCompose(lambda x: x.strip())

