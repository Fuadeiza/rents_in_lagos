# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentsInLagosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



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
    crawled = Field()  # Crawl datetime

    # Required
    location = Field()  # response.url
    house_type = Field()  # HTML dump of body section
    price = Field()  # URL of the document file




class FileItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    location_in = MapCompose(str.strip)
    location_out = Join()

    house_type_in = MapCompose(str.strip)
    house_type_out = Join()

    price_in = MapCompose(str.strip)
    price_out = Join()





