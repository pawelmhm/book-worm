# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
#
from __future__ import print_function

import logging
import zipfile
from io import BytesIO
from os import path

import dateparser
import djvu.decode
import pdfminer.high_level

from scrapy import Request
from slugify import slugify
import sys

logger = logging.getLogger(__name__)

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
        buffer = BytesIO()
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
        djvu_url = item.get('djvu_url')
        pdf_url = item.get('pdf_url')
        if djvu_url:
            callback = self.parse_djvu
            url = djvu_url
        elif pdf_url:
            callback = self.parse_pdf
            url = pdf_url
        else:
            logger.error('missing resource url {}'.format(item.get('title')))
            return

        request = Request(url, meta={
            'item': item
        })
        dfd = self.crawler.engine.download(request, spider)
        dfd.addCallbacks(callback=callback, errback=self.finish)
        return dfd

    def parse_djvu(self, response):
        item = response.meta['item']
        content_id = item['title']
        store_path = path.join(STORE_PATH, slugify(content_id))
        item['file_path'] = store_path
        buffer = BytesIO(response.body)
        zip_file = zipfile.ZipFile(buffer)
        zip_file.extractall(store_path)
        index_path = path.join(store_path, self.crawler.spider.djvu_root_file)
        context = Context()
        text = context.process(index_path)
        item['text'] = text
        return item

    def parse_pdf(self, response):
        item = response.meta['item']
        response_file = BytesIO(response.body)
        output = BytesIO()
        pdfminer.high_level.extract_text_to_fp(response_file, output)
        text = output.getvalue()

        text = text[:100]
        item['text'] = text
        return item

    def finish(self, response):
        return response.meta['item']



class DefaultValuesPipeline(object):

    def process_item(selfse, item, spider):
        item['crawl_id'] = spider.crawl_id
        item['publication_name'] = spider.name
        publication_date = item.pop('publication_date_raw', '')
        if publication_date:
            new_date = dateparser.parse(publication_date)
            if new_date:
                item['publication_date'] = new_date.isoformat()
        return item
