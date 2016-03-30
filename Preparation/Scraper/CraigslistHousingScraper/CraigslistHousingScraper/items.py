# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CraigslistItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    address = Field()
    sqft = Field()
    numImages = Field()
    description = Field()
    price = Field()
    postingDate = Field()
    updateDate = Field()
    latitude = Field()
    longitude = Field()
    #reposts = Field()
    zipcode = Field()
    bedrooms = Field()
    bathrooms = Field()
    link = Field()
