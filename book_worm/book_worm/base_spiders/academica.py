import re

from furl import furl, urljoin

from book_worm.base_spiders.base import BaseSpider
from book_worm.items import BookWormItemLoader


class BaseAcademicaSpider(BaseSpider):
    pdf_link = 'https://academica.edu.pl/archive/{cid}?uid={uid}&cid={cid}'

    def parse(self, response):
        for link in response.css('a.wrapLinks')[:5]:
            title = link.xpath("./text()").get()
            href = link.xpath("./@href").get()
            if not re.search('nr', title):
                continue
            yield response.follow(href, callback=self.parse_issue)

    def parse_issue(self, response):
        pdf_url = response.css('.download-contents a::attr(href)').get()
        url = furl(urljoin(response.url, pdf_url))
        cid = url.args.popvalue('cid')
        uid = url.args.popvalue('uid')
        loader = BookWormItemLoader(selector=response)
        loader.add_xpath('title', "//label[contains(text(), 'Iteracja')]/following-sibling::ul/li/text()")
        title = loader.load_item().get('title')
        loader.add_value('publication_date_raw', title, re='\(.+?\)')
        loader.add_value('content_id', cid + uid)
        loader.add_value('pdf_url', self.pdf_link.format(cid=cid, uid=uid))
        return loader.load_item()
