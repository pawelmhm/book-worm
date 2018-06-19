import datetime
import hashlib
import re
from urlparse import urljoin

import scrapy
from scrapy import Request

from book_worm.items import BookWormItemLoader


class BaseDlibraSpider(scrapy.Spider):
    root_url = ''
    publication_id = ''
    year_regex = ''
    item_limit = 0
    zip_url = '{}/Content/{}/zip/'
    djvu_root_file = 'index.djvu'
    limit_start = 0
    limit_end = 1000

    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "{}/dlibra/publication?id={}".format(
                self.root_url, self.publication_id
            )
        ]
        self.crawl_id = hashlib.md5(
            self.name + datetime.datetime.now().isoformat()).hexdigest(

        )

    def parse(self, response):
        for x in response.css("#struct > ul > li > ul li a.item-content"):
            href = x.xpath("./@href").get()
            title = x.xpath("./text()").get()
            if self.year_regex and title:
                if not re.search(self.year_regex, title):
                    continue
            yield Request(href, callback=self.parse_year)

    def parse_year(self, response):
        link_path = "#struct > ul > li > ul li a.contentTriggerStruct"

        for book in response.css(link_path)[self.limit_start:self.limit_end]:
            loader = BookWormItemLoader(selector=book)
            loader.add_xpath("title", "./@title")
            # loader.add_xpath("_id", "./@title", MapCompose(
            #    lambda x: hashlib.md5(x).hexdigest()
            # ))
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

        djvu_url = djvu_url.group(1).replace('index.djvu', 'zip/')
        content_id = re.search("Content/(\d+)/", djvu_url).group(1)
        loader.add_value('djvu_url', self.zip_url.format(self.root_url, content_id))
        loader.add_value('content_id', content_id)
        return loader.load_item()