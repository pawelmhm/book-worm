import datetime
import hashlib

import scrapy


class BaseSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        dt = self.name + datetime.datetime.now().isoformat()
        self.crawl_id = hashlib.md5(dt.encode('utf8')).hexdigest()
        super(BaseSpider, self).__init__(*args, **kwargs)
