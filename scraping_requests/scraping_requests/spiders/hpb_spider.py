import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HpbSpiderSpider(CrawlSpider):
    name = "hpb_spider"
    start_urls = "https://beauty.hotpepper.jp/pre13/"

    def start_requests(self):
        yield scrapy.Request(self.start_urls, dont_filter=True)

    rules = (Rule(LinkExtractor(restrict_xpaths='//h3[@class="slnName"]/a'), 
                  callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths='//span[@class="iS arrowPagingR"]/parent::a'),
                 follow=True)
            )

    def parse_item(self, response):
        salon_name = response.xpath('//p[@class="detailTitle"]/a/text()').get()
        if salon_name:
            salon_name = re.sub('\s', '', salon_name)

        salon_url = response.url

        number_of_seats = response.xpath('//th[text()="席数"]/following-sibling::td/text()').get()
        if number_of_seats:
            number_of_seats = re.sub('\s', '', number_of_seats)
            
        stylists = response.xpath('//th[text()="スタッフ数"]/following-sibling::td[1]/text()').get()
        if stylists:
            stylists = re.sub('\s', '', stylists)

        yield {
            "salon_name" : salon_name,
            "salon_url" : salon_url,
            "number_of_seats" : number_of_seats,
            "stylists" : stylists
        }
