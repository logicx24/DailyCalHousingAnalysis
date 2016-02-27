# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings



class MongoPipe(object):

    def __init__(self):
		self.server = settings['MONGODB_SERVER']
		self.port = settings['MONGODB_PORT']
		self.client = pymongo.MongoClient(self.server, self.port)
		self.db = self.client.HousingListings
		self.itemCollection = self.db.listings
		self.repeatsCollection = self.db.usedLinks	

    def process_item(self, item, spider):
    	insertedId = self.itemCollection.insert(dict(item))
    	rep = self.repeatsCollection.insert({"link": item['link'], 'obj': insertedId})
        return item

