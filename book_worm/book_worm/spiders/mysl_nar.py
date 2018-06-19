# -*- coding: utf-8 -*-

from book_worm.base_spiders.dlibra import BaseDlibraSpider


class MyslNarSpider(BaseDlibraSpider):
    name = 'mysl_narodowa'
    root_url = 'http://www.wbc.poznan.pl'
    publication_id = '139164'
    year_regex = '1926'
    limit_start = 10
    limit_end = 50
    # djvu_root_file = 'directory.djvu'
