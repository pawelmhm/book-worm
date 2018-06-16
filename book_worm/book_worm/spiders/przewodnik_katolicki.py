# -*- coding: utf-8 -*-

from book_worm.base_spiders.dlibra import BaseDlibraSpider


class PrzewodnikKatolicki(BaseDlibraSpider):
    name = 'przewodnik_katolicki'
    root_url = 'http://www.wbc.poznan.pl'
    publication_id = "172396"
    year_regex = r"193[0-4]"
