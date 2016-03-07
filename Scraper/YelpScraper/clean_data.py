import json

with open('data_sample.json') as ha:
	data = json.load(ha)

print data["total"]