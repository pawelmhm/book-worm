# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
#
from __future__ import print_function
import zipfile
from StringIO import StringIO
from os import path

import djvu.decode

from scrapy import Request
from slugify import slugify
import sys


def print_text(sexpr, buffer):
    if isinstance(sexpr, djvu.sexpr.ListExpression):
        if len(sexpr) == 0:
            return
        for child in sexpr[5:]:
            print_text(child, buffer)
    else:
        buffer.write(" " + sexpr.bytes.decode('utf8').replace("\"", ""))


class Context(djvu.decode.Context):

    def handle_message(self, message):
        # noinspection PyPackageRequirements
        if isinstance(message, djvu.decode.ErrorMessage):
            print(message, file=sys.stderr)
            # TODO exceptions in djvu parsing hang whole process, why?
            return

    def process(self, path):
        document = self.new_document(djvu.decode.FileURI(path))
        document.decoding_job.wait()
        buffer = StringIO()
        for page in document.pages:
            page.get_info()
            print_text(page.text.sexpr, buffer)
        return buffer.getvalue()


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
        store_path = path.join(STORE_PATH, slugify(content_id))
        item['file_path'] = store_path
        buffer = StringIO(response.body)
        zip_file = zipfile.ZipFile(buffer)
        zip_file.extractall(store_path)
        index_path = path.join(store_path, 'index.djvu')
        context = Context()
        text = context.process(index_path)
        item['text'] = text
        return item

    def finish(self, response):
        return response.meta['item']
