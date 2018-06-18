# -*- coding: utf-8 -*-
from book_worm.base_spiders.dlibra import BaseDlibraSpider


class WarszawskiDziennikSpider(BaseDlibraSpider):
    name = 'warszawski_dziennik'
    root_url = 'http://ebuw.uw.edu.pl'
    year_regex = '1935'
    djvu_root_file = 'directory.djvu'
    publication_id = '77915'
