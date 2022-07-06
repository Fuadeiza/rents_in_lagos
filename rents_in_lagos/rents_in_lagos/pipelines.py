# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import pymongo
import sys
from scrapy.exceptions import DropItem

from .items import FileItem


class RentsInLagosPipeline:
    def process_item(self, item, spider):
        required_item_fields = ["house_type", "price", "location"]
        if all(field in item.keys() for field in required_item_fields):
            item["crawled"] = datetime.now()
            return item
        else:
            missing_fields = [
                field for field in required_item_fields if field not in item.keys()
            ]
            raise DropItem(f"Missing item fields: {missing_fields}")


class MongoDBPipeline:

    collection = 'scrapy_items'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(FileItem(item))
        self.db[self.collection].insert_one(data)
        return item