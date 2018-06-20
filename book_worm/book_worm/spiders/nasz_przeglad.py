# -*- coding: utf-8 -*-
from book_worm.base_spiders.academica import BaseAcademicaSpider


class NaszPrzegladSpider(BaseAcademicaSpider):
    name = 'nasz_przeglad'
    start_urls = ['https://academica.edu.pl/reading/readStruct?cid=9490325&page=1&uid=9156101']
