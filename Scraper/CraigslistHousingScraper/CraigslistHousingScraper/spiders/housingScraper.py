# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from CraigslistHousingScraper.items import CraigslistItem
import datetime
import time
import pymongo
from scrapy.conf import settings


class HousingscraperSpider(CrawlSpider):
    name = "housingScraper"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = [
        'http://sfbay.craigslist.org/search/apa?s=0&query=berkeley'
    ]

    rules = [
    	Rule(LinkExtractor(allow="http:\/\/sfbay\.craigslist\.org\/search\/", deny="http:\/\/sfbay\.craigslist\.org\/eby\/apa\/", \
            restrict_xpaths=["//*[@id='searchform']/div[4]", "//*[@id='searchform']/div[5]/div[3]/span[2]/a[3]"]),\
            follow=True),

    	Rule(LinkExtractor(allow="http:\/\/sfbay\.craigslist\.org\/eby\/apa\/", \
            deny=["http:\/\/sfbay\.craigslist\.org\/search\/"]), \
            callback='parse_listing', follow=False)
    ]

    def parse_listing(self, response):
        item = CraigslistItem()

        #stolen (and modified) from some dude on the internet cause fuck xpath - https://github.com/jayfeng1/Craigslist-Pricing-Project/blob/master/craigslist/spiders/CraigSpyder.py
        #
        #temp = postings[i].xpath("span[@class='txt']")
        #info = temp.xpath("span[@class='pl']")
        #title of posting
        item["title"] = response.xpath("//*[@id='titletextonly']/text()").extract()[0]
        #date of posting
        curr = response.xpath("//*[@id='pagecontainer']/section/section/div[2]/p[2]/time/text()").extract()[0].split()[0]
        item["postingDate"] = int(time.mktime(datetime.datetime.strptime(curr, "%Y-%m-%d").timetuple()))
        #pre-processing for getting the price in the right format
        #item["area"] = ''.join(temp.xpath("span")[2].xpath("span[@class='pnr']").xpath("small/text()").extract())
        item["price"] = int(response.xpath("//*[@id='pagecontainer']/section/h2/span[2]/span[1]/text()").extract()[0].replace("$",""))#price.replace("$","")
        item["link"] = response.url

        maplocation = response.xpath("//div[contains(@id,'map')]")
        latitude = ''.join(maplocation.xpath('@data-latitude').extract())
        longitude = ''.join(maplocation.xpath('@data-longitude').extract())
        tmp = response.xpath("//*[@id='pagecontainer']/section/section/div[1]/div[1]/div[2]/text()").extract()
        if len(tmp) > 0:
            item['address'] = tmp[0]
        if latitude:
            item['latitude'] = float(latitude)
        if longitude:
            item['longitude'] = float(longitude)
        attr = response.xpath("//p[@class='attrgroup']")
        try:
            item["bedrooms"] = int(attr.xpath("span/b/text()")[0].extract())
        except:
            pass
        try:
            bath = attr.xpath("span/b/text()")[1].extract()
        except:
            pass
        try:    
            item["sqft"] = int(''.join(attr.xpath("span")[1].xpath("b/text()").extract()))
        except:
            pass
        try:
            if(bath.isdigit()):
                item["bathrooms"] = int(attr.xpath("span/b/text()")[1].extract())
            item["bathrooms"] = int(bath)
        except:
            pass

        item['description'] = "".join(response.xpath("//section[@id='postingbody']").xpath("text()").extract()) 
        item["numImages"] = len(response.xpath("//div[@id='thumbs']").xpath("a"))
        return item
