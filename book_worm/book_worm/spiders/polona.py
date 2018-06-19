# -*- coding: utf-8 -*-
import json
from urllib import quote_plus

import scrapy


class PolonaSpider(scrapy.Spider):
    name = 'polona'
    search_url = 'https://polona.pl/api/entities/?size=55&query={}&filters=public%3A1'
    query = 'nasz przegląd organ niezależny 1934'

    def start_requests(self):
        url = self.search_url.format(quote_plus(self.query))
        yield scrapy.Request(url, headers={
            'Accept': 'application/json'
        })

    def parse(self, response):
        data = json.loads(response.body)
