# -*- coding: utf-8 -*-
import re
from urlparse import urljoin

import scrapy

from book_worm.items import BookWormItemLoader
from scrapy import Request


class DlibraSpider(scrapy.Spider):
    name = 'przewodnik_katolicki'
    start_urls = ['http://www.wbc.poznan.pl/dlibra/publication?id=172396']
    root_url = 'http://www.wbc.poznan.pl'

    def parse(self, response):
        for x in response.css("#struct > ul > li > ul li a.item-content::attr(href)").extract():
            yield Request(x, callback=self.parse_year)
            break

    def parse_year(self, response):
        link_path = "#struct > ul > li > ul li a.contentTriggerStruct"

        for book in response.css(link_path):
            loader = BookWormItemLoader(selector=book)
            loader.add_xpath("title", "./@title")
            loader.add_value("year_url", response.url)
            djvu_page_url = book.xpath("./@href").get()

            if not djvu_page_url:
                self.logger.error('no url {}'.format(response))
                continue
            yield Request(djvu_page_url, callback=self.parse_issue, meta={
                'item': loader.load_item()
            })

    def parse_issue(self, response):
        item = response.meta['item']
        loader = BookWormItemLoader(item)
        djvu_url = re.search('content_url=(.+)\'', response.body)
        if not djvu_url:
            self.logger.error('no djvu')
            return
        loader.add_value('djvu_url', urljoin(self.root_url, djvu_url.group(1)))
        return loader.load_item()
