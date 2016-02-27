import pymongo
from scrapy.dupefilter import RFPDupeFilter
from scrapy.conf import settings


class CustomDupeFilter(RFPDupeFilter):

	def __init__(self, path=None, other=None):
		inmem = [str(it['link']) for it in pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']).HousingListings.usedLinks.find()]
		self.already_seen = set(inmem)
		RFPDupeFilter.__init__(self, path, other)

	def request_seen(self, request):
		if request.url in self.already_seen:
			return True
		else:
			self.already_seen.add(request.url)
			


