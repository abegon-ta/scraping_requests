import re
import requests
from lxml import html

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

        address = response.xpath('//th[text()="住所"]/following-sibling::td/text()').get()
        if address:
            address = re.sub('\s', '', address)
        
        tel_url = response.xpath('//th[text()="電話番号"]/following-sibling::td/a/@href').get()
        if tel_url:
            res_for_tel = requests.get(tel_url)
            res_for_tel = html.fromstring(res_for_tel.text)
            tel = res_for_tel.xpath('//th[text()="電話番号  "]/following-sibling::td/text()')
            if tel:
                tel = re.sub('\s', '', tel[0])

        number_of_seats = response.xpath('//th[text()="席数"]/following-sibling::td/text()').get()
        if number_of_seats:
            number_of_seats = re.sub('\s', '', number_of_seats)
            
        stylists = response.xpath('//th[text()="スタッフ数"]/following-sibling::td[1]/text()').get()
        if stylists:
            stylists = re.sub('\s', '', stylists)
        

        yield {
            "salon_name" : salon_name,
            "salon_url" : salon_url,
            "address" : address,
            "tel" : tel,
            "number_of_seats" : number_of_seats,
            "stylists" : stylists
        }
