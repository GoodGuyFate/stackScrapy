# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from scrapy import settings
from scrapy.exceptions import DropItem
import logging

logger = logging.getLogger("mycustomlogger")

class StackPipeline:
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):

    def __init__(self, crawler):  # Inject the crawler object
        self.crawler = crawler  # Store the crawler object

        # Establish a single connection (consider connection pooling for efficiency)
        self.connection = pymongo.MongoClient(
            self.crawler.settings.get('MONGODB_SERVER'),
            self.crawler.settings.get('MONGODB_PORT', 27017)  # Default port
        )
        db = self.connection[self.crawler.settings.get('MONGODB_DB')]
        self.collection = db[self.crawler.settings.get('MONGODB_COLLECTION')]

    @classmethod
    def from_crawler(cls, crawler):  # Factory method for cleaner initialization
        return cls(crawler)

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem(f"Missing data for field '{data}'!")

        if valid:
            self.collection.insert_one(dict(item))  # Use insert_one for clarity
            logger.debug("Question added to MongoDB database!", spider=spider)
        return item
            
