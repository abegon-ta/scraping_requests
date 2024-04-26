import re

import scrapy


class ReservaSpiderSpider(scrapy.Spider):
    name = "reserva_spider"
    start_urls = "https://reserva.be/ginyamakohoku/about"

    def start_requests(self):
        #TODO urlをiterationする機構に切り替える    
        yield scrapy.Request(self.start_urls, dont_filter=True)

    def parse(self, response):
        shop_url = response.url
        site_title = response.xpath("//div[@class='header_container']//a/text()[2]").get()
        if site_title:
            site_title = re.sub("\s", "", site_title)
        tel = response.xpath("//dt[text()='お問い合わせ電話番号']/following-sibling::dd/span/text()").get()
        if tel:
            tel = re.sub("\s", "", tel)
        location_list = response.xpath("//div[@class='card about-us__information']//dt[text()='所在地']/following-sibling::dd/text()").getall()
        if location_list:
            location = re.sub("\s", "", "".join(location_list))
        description_list = response.xpath("//div[@class='card about-us__description']/p/text()").getall()
        if description_list:
            description = re.sub("\s", "", "".join(description_list))

        yield {
            "shop_url": shop_url,
            "site_title": site_title,
            "tel": tel,
            "location": location,
            "description": description
        }
