# -*- coding: utf-8 -*-
import scrapy


class OshaSpider(scrapy.Spider):
    name = "osha"
    allowed_domains = ["osha.gov"]
    start_urls = (
        'https://www.osha.gov/dsg/annotated-pels/tablez-1.html',
    )

    def parse(self, response):
        for row in response.css('#z-1 tbody tr'):
            cells = row.css('td::text').extract()
            if len(cells) == 7:
                yield {
                    'substance': cells[0],
                    'cas_no': cells[1],
                    'pel_ppm': cells[2],
                    'pel_mg_m3': cells[3]
                }
