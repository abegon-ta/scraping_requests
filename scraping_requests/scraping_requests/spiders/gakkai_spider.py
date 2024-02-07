import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class GakkaiSpiderSpider(CrawlSpider):
    name = "gakkai_spider"
    start_urls = "https://jams.med.or.jp/members-s/"

    def start_requests(self):
        yield scrapy.Request(self.start_urls, dont_filter=True)

    rules = (Rule(LinkExtractor(restrict_xpaths="//ul[@id='mslist']/li/a"),
                                 callback="parse_item", follow=True),)

    def parse_item(self, response):
        society_name = response.xpath("//p[@class='name']/span[@class='j']/text()").get()
        address_info = response.xpath("//p[text()='事務局所在地']/following-sibling::p[1]/text()").getall()
        if address_info:
            post_code = [x for x in address_info if "〒" in x]
            if post_code:
                post_code = re.sub('〒', '', post_code[0])
            else:
                post_code = None
            tel_fax = [x for x in address_info if "Tel" in x or ""]
            if tel_fax:
                tel = re.findall('Tel：(\d{2,4}（\d{2,4}）\d{4})', tel_fax[0])
                if tel:
                    tel = tel[0]
                else:
                    tel = None
                fax = re.findall('Fax：(\d{2,4}（\d{2,4}）\d{4})', tel_fax[0])
                if fax:
                    fax = fax[0]
                else:
                    fax = None
            else:
                tel = None
                fax = None
            address = [x for x in address_info if "〒" not in x and "Tel" not in x and "E-mail" not in x]
            if address:
                address = re.sub('\s', '',  ("".join(address)))
            else:
                address = None
        email = response.xpath("//p[text()='事務局所在地']/following-sibling::p[1]/a/@href").get()
        hp = response.xpath("//p[text()='学会ホームページ']/following-sibling::p[1]/a/@href").get()
        member_num = response.xpath("//p[text()='会員数']/following-sibling::p[1]/text()").get()
        membership_fee = response.xpath("//p[text()='会費']/following-sibling::p[1]/text()").getall()
        if membership_fee:
            membership_fee = re.sub('\s', '', ("".join(membership_fee)))

        yield {
            'society_name' : society_name,
            'address' : address,
            'email' : email,
            'tel' : tel,
            'fax' : fax,
            'post_code' : post_code,
            'address' : address,
            'hp' : hp,
            'member_num' : member_num,
            'membership_fee' : membership_fee
        }
