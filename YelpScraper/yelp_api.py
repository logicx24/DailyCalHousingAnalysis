# source activate python2

import sample as s 
import json

api = 'FmI5xWeT7qEqfRRrPRL8tQ'

""" Search Parameters """
limit = 1
term = 'food'
location = 'berkeley'
offset = 0 #Offset the list of returned business results by this amount
category_filter = "null"
radius_filter = 0 #in meters

# Search Bound
southwest_lat = 37.853727
southwest_long = -122.278823
northeast_lat = 37.884056
northeast_long = -122.251139
#bound = southwest_lat,southwest_long,northeast_lat,northeast_long
bound = str(southwest_lat) +','+ str(southwest_long) +'|'+ str(northeast_lat) +','+ str(northeast_long)

# Specific Locatioin
latitude = 37.853727
longitude = -122.278823
cll = str(latitude) + ',' + str(longitude)

# parameter: term, location, limit, cll, bounds
request = s.search(term, bounds = bound)

with open('yelp_data.json', 'w') as fp:
    json.dump(request, fp)
