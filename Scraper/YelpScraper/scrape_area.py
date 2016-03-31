import json
import sample as s

def bound(southwest_lat, southwest_long, northeast_lat, northeast_long):
	return str(southwest_lat) +','+ str(southwest_long) +'|'+ str(northeast_lat) +','+ str(northeast_long)


southwest_lat = 37.853727
southwest_long = -122.278823
northeast_lat = 37.884056
northeast_long = -122.251139

b = bound(southwest_lat, southwest_long, northeast_lat, northeast_long)

request = s.search(term = 'food', limit = 30, bounds = b)
with open('test.json', 'a') as fp:
	json.dump(request, fp)