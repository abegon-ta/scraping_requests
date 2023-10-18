import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HaikuSpiderSpider(CrawlSpider):
    name = "haiku_spider"
    # start_urls = ["https://haiku-data.jp/author_list.php"]
    start_url = "https://haiku-data.jp/author_list.php"
    
    def start_requests(self):
        yield scrapy.Request(self.start_url, dont_filter=True)

    rules = (Rule(LinkExtractor(restrict_xpaths=('//td[@width="215"]/a'),
                                attrs=('href')), 
                  follow=True),

             Rule(LinkExtractor(restrict_xpaths=('//div[@align="center"]//following-sibling::table[1]//div[@class="font6"]/a'),
                                attrs=('href')), 
                  callback="parse_item", follow=True))
          

    def parse_item(self, response):
        haiku = response.xpath('//div[@class="title"]/b/text()').get()
        if haiku:
            haiku = re.sub("&nbsp", "", haiku)
        kigo = response.xpath('//table//font[text()="季　語"]/ancestor::td/following-sibling::td/div/text()').get()
        if kigo:
            kigo = re.sub("&nbsp", "", kigo)
        season = response.xpath('//table//font[text()="季　節"]/ancestor::td/following-sibling::td/div/text()').get()
        if season:
            season = re.sub("&nbsp", "", season)
        author = response.xpath('//table//font[text()="作　者"]/ancestor::td/following-sibling::td/div/text()').get()
        if author:
            author = re.sub("&nbsp", "", author)

        yield {
            "haiku" : haiku,
            "kigo" : kigo,
            "season" : season,
            "author" : author
        }



#実行コマンド
# scrapy crawl haiku_spider -o ../scraped_data/data.json