# -*- coding: utf-8 -*-
import scrapy


class OshaSpider(scrapy.Spider):
    name = "osha"
    allowed_domains = ["osha.gov"]
    start_urls = (
        'https://www.osha.gov/dsg/annotated-pels/tablez-1.html',
    )


    def parse(self, response):
        def isSpan(td):
            return td.xpath('colspan').extract_first() is not None

        for row in response.css('#z-1 tbody tr'):
            cells = row.css('td')
            if len(cells) < 4:
                continue
            if any(isSpan(elem) for elem in cells[:4]):
                # see "Beryllium and beryllium compounds (as Be)"
                # on table Z-1 for an example of what this is trying
                # to skip
                continue
            yield {
                'substance': cells[0].xpath('text()').extract_first(),
                'cas_no': cells[1].xpath('text()').extract_first(),
                'pel_ppm': cells[2].xpath('text()').extract_first(),
                'pel_mg_m3': cells[3].xpath('text()').extract_first()
            }


