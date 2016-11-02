import numpy as np
import pymongo
from geopy.distance import vincenty
import datetime

from math import cos

#Choose one.
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import Imputer
from sklearn import cross_validation

import requests
from lxml import html
import time
import json
import csv

def mongoConnection():
    return pymongo.MongoClient().HousingListings.listings

def jsonDump():
    with open("listings.json", 'w') as out:
        listings = list(mongoConnection().find({
                              "latitude": {"$exists": True},
                              "longitude": {"$exists": True},
                              "numImages": {"$exists": True},
                              "description": {"$exists": True},
                             }))
        print(len(listings))
        for i in range(len(listings)):
            listings[i].pop("_id")
        json.dump({"listings" :listings}, out, ensure_ascii=True)

class Classifier(object):

    def __init__(self, training_data_csv="training_data.csv", json_dump_reader="listings.json"):
        self.training_data_csv = training_data_csv
        self.json_dump_reader = json_dump_reader
        self.now = datetime.datetime.now()

    def featurize(self, listing):
        if "bedrooms" in listing:
            bedrooms = listing["bedrooms"]
        else:
            bedrooms = np.nan

        if "bathrooms" in listing:
            bathrooms = listing["bathrooms"]
        else:
            bathrooms = np.nan

        if "sqft" in listing:
            sqft = listing["sqft"]
        else:
            sqft = np.nan

        if "latitude" in listing and "longitude" in listing:
            #distance = self.get_distance(listing['latitude'], listing['longitude'])
            distance = self.bounding_dist(listing['latitude'], listing['longitude'])
        else:
            distance = np.nan
       
        images = listing['numImages']
        uniqueWords = len(listing['description'].split(" "))

        time_up = (self.now - datetime.datetime.fromtimestamp(listing['postingDate'])).days

        return np.array([bedrooms, bathrooms, sqft, distance, images, uniqueWords, time_up])

    def cols(self):
        return ['bedrooms', 'bathrooms', 'sqft', 'distance_to_campus', 'num_images', 'unique_words', 'postingDate', 'price']

    def get_distance(self, lat, lon):
        center = (37.872105, -122.259470)
        return vincenty(center, (lat, lon)).miles 

    def bounding_dist(self, lat, lon):

        top_left_t = (37.874185, -122.266381)
        bot_right_t = (37.869671, -122.252347)

        def long_dist_func(lat):
            return cos(lat) * lat_dist_func()

        def lat_dist_func():
            return 69.172

        lat_dist = min(abs(lat - top_left_t[0])*lat_dist_func(), abs(lat-bot_right_t[0])*lat_dist_func())
        lon_dist = min(long_dist_func(lat)*abs(top_left_t[1] - lon), long_dist_func(lat)*abs(bot_right_t[1] - lon))
        return (lat_dist**2 + lon_dist**2)**0.5

    def featurized(self, cursor):
        x = []
        y = []
        for listing in cursor:
            x.append(self.featurize(listing))
            y.append(listing['price'])
        return np.array(x), np.array(y)

    def pullListings(self):
        return json.loads(open(self.json_dump_reader).read())['listings']

    def csvToArray(self):
        x = []
        y = []
        with open(self.training_data_csv) as fin:
            reader = csv.reader(fin)
            reader.next()
            for row in reader:
                y.append(float(row[-1]))
                x.append([float(val) for val in row[:-1]])
        x = np.array(x)
        y = np.array(y)
        imp, x_imp = self.genImputer(x, "median")

        self.feats = x_imp
        self.labels = y
        self.imp = imp


    def genImputer(self, arr, strat):
        imp = Imputer(missing_values="NaN", strategy=strat, axis=0, copy=True)
        return imp, imp.fit_transform(arr)

    def csvDump(self):
        listings = self.pullListings()
        x, y = self.featurized(listings)
        appd = np.hstack((x, y[np.newaxis].T))
        with open(self.training_data_csv, 'w') as out:
            writer = csv.writer(out)
            writer.writerow(self.cols())
            for i in range(len(appd)):
                writer.writerow(list(appd[i]))

    def linkToVector(self, link):
        r = requests.get(link)
        response = tree = html.fromstring(r.text)
        
        item = {}
        curr = response.xpath("//*[@id='pagecontainer']/section/section/div[2]/p[2]/time/text()")[0].split()[0]
        item["postingDate"] = int(time.mktime(datetime.datetime.strptime(curr, "%Y-%m-%d").timetuple()))
        item["price"] = int(response.xpath("//*[@id='pagecontainer']/section/h2/span[2]/span[1]/text()")[0].replace("$",""))
        maplocation = response.xpath("//div[contains(@id,'map')]")
        latitude = ''.join(maplocation[0].xpath('@data-latitude'))
        longitude = ''.join(maplocation[0].xpath('@data-longitude'))
        tmp = response.xpath("//*[@id='pagecontainer']/section/section/div[1]/div[1]/div[2]/text()")

        chars_to_remove = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if len(tmp) > 0:
            item['address'] = tmp[0]
        if latitude:
            item['latitude'] = float(latitude)
        if longitude:
            item['longitude'] = float(longitude)
        try:
            item["bedrooms"] = float(response.xpath("//*[@id='pagecontainer']/section/section/div[1]/p[1]/span[1]/b[1]/text()")[0].translate(None, chars_to_remove))
        except IndexError:
            pass
        try:
            item["sqft"] = float(response.xpath("//*[@id='pagecontainer']/section/section/div[1]/p[1]/span[2]/b/text()")[0].translate(None, chars_to_remove))
        except IndexError:
            pass
        try:    
            item["bathrooms"] = float(response.xpath("//*[@id='pagecontainer']/section/section/div[1]/p[1]/span[1]/b[2]/text()")[0].translate(None, chars_to_remove))
        except IndexError:
            pass
        item['description'] = "".join(response.xpath("//section[@id='postingbody']/text()"))
        item["numImages"] = len(response.xpath("//div[@id='thumbs']/a"))
        return self.featurize(item)

    def train(self):
        final = Ridge(alpha=.1)
        self.csvToArray()
        final.fit(self.feats, self.labels)
        self.model = final

    def predictionFromLink(self, link):
        vector = self.imp.transform(self.linkToVector(link))
        return self.model.predict(vector)

    def predict(self, vector):
        return self.model.predict(self.imp.transform(vector))

    def cross_validate(self, alpha=.1):
        final = Ridge(alpha=alpha)
        self.csvToArray()
        return cross_validation.cross_val_score(final, self.feats, self.labels, cv=10)

if __name__ == "__main__":
    jsonDump()
    classifier = Classifier()
    classifier.csvDump()
    classifier.train()
    for alpha in [0.001, 0.01, 0.1, 1, 10, 0.8]:
        print "-------------------------------------------"
        print alpha
        scores = classifier.cross_validate(alpha)
        print scores
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        print "-------------------------------------------"
    # classifier.train()
    print classifier.predictionFromLink("http://sfbay.craigslist.org/eby/apa/5849230189.html")


