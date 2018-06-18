# -*- coding: utf-8 -*-

from book_worm.base_spiders.dlibra import BaseDlibraSpider


class GazetaWarszawskaSpider(BaseDlibraSpider):
    name = 'gazeta_warszawska'
    publication_id = '286828'
    root_url = 'http://ebuw.uw.edu.pl'
    year_regex = '1923'
    item_limit = 10
    djvu_root_file = 'directory.djvu'
