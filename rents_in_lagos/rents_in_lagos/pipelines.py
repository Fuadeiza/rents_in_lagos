# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

from scrapy.exceptions import DropItem


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