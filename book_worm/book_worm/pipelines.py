# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
#
import zipfile
from StringIO import StringIO

import djvu.decode

from scrapy import Request
from slugify import slugify


def print_text(sexpr, level=0):
    if level > 0:
        print(' ' * (2 * level - 1))
    if isinstance(sexpr, djvu.sexpr.ListExpression):
        if len(sexpr) == 0:
            return
        print(str(sexpr[0].value), [sexpr[i].value for i in range(1, 5)])
        for child in sexpr[5:]:
            print_text(child, level + 1)
    else:
        print(sexpr)


class Context(djvu.decode.Context):

    def handle_message(self, message):
        if isinstance(message, djvu.decode.ErrorMessage):
            print(message)

    def process(self, path):
        document = self.new_document(djvu.decode.FileURI(path))
        document.decoding_job.wait()
        for page in document.pages:
            page.get_info()
            print_text(page.text.sexpr)

STORE_PATH = '/home/pawel/Documents/journals'


class BookWormPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        djvu_url = item['djvu_url']
        assert djvu_url

        request = Request(djvu_url, callback=self.parse_djvu, meta={
            'item': item
        }, errback=self.finish)
        dfd = self.crawler.engine.download(request, spider)
        dfd.addCallbacks(callback=self.parse_djvu, errback=self.finish)
        return dfd

    def parse_djvu(self, response):
        item = response.meta['item']
        content_id = item['title']
        store_path = STORE_PATH + '/' + slugify(content_id)
        item['file_path'] = store_path
        buffer = StringIO(response.body)
        zip_file = zipfile.ZipFile(buffer)
        zip_file.extractall(store_path)
        return item

    def finish(self, response):
        return response.meta['item']
