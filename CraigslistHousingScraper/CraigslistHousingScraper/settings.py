# -*- coding: utf-8 -*-

# Scrapy settings for CraigslistHousingScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from fake_useragent import UserAgent

BOT_NAME = 'CraigslistHousingScraper'

MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017

SPIDER_MODULES = ['CraigslistHousingScraper.spiders']
NEWSPIDER_MODULE = 'CraigslistHousingScraper.spiders'

ITEM_PIPELINES = (
	'CraigslistHousingScraper.pipelines.MongoPipe',
)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
ua = UserAgent()
USER_AGENT = ua.random
