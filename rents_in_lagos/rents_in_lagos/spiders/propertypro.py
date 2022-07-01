import scrapy


class PropertyproSpider(scrapy.Spider):
    name = 'propertypro'
    allowed_domains = ['www.propertypro.ng']
    start_urls = ['http://www.propertypro.ng/']

    def parse(self, response):
        pass
