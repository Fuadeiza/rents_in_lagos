# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader




class FileItem(Item):
    """See pipelines.PublishersPipeline for fields that need to be returned"""
    # Auto generated in PublishersPipeline
    # crawled = Field()  # Crawl datetime

    # Required
    location = scrapy.Field()  # response.url
    house_type = scrapy.Field(output_processor=TakeFirst()) # HTML dump of body section
    price = scrapy.Field(output_processor=TakeFirst()) # URL of the document file







