
import json
import csv


with open('yelp.json') as d:
    RAW = d.read()
RAW = '[' + RAW.replace('}{', '},{') + ']'
rest = json.loads(RAW)

# Clean1: get rid of extra info
## Target format: [{'latitude': xxx, 'longtitude': xxx,'businesses': [{'categories': xxx, 'name': xxx, 'rating': xxx, 'neighborhoods': xxx}, {}, {}...]}, {}, {} ...]

new = []
num_loc = len(rest)
for i in range(num_loc):
    one_loc = {}
    businesses = []
    one_loc['latitude'] = rest[i]['region']['center']['latitude']
    one_loc['longitude'] = rest[i]['region']['center']['longitude']
    # businesses
    num_bus = len(rest[i]['businesses'])
    for j in range(num_bus):    
        try:
            one_bus = rest[i]['businesses'][j]
        except:
            import pdb; pdb.set_trace()
        new_bus = {}
        new_bus['categories'] = one_bus['categories'][0][0]
        new_bus['name'] = one_bus['name']
        new_bus['rating'] = one_bus['rating']
        businesses.append(new_bus)
    one_loc['businesses'] = businesses
    new.append(one_loc)

json_str = json.dumps(new)
with open('yelp_clean1.json', 'w') as d:
    json.dump(json_str, d)


# Clean2: Average rating & #Cafes & #Pubs
analysis = []
for i in range(len(new)):
    loc = {}
    loc['latitude'] = new[i]['latitude']
    loc['longitude'] = new[i]['longitude']
    total = 0
    num_bus = len(new[i]['businesses'])
    for j in range(num_bus):
        total += new[i]['businesses'][j]['rating']
    loc['avg_rating'] = float(total) / float(num_bus)
    
    cafe = 0
    pub = 0
    num_bus = len(new[i]['businesses'])
    for j in range(num_bus):
        if ('Coffee' in new[i]['businesses'][j]['categories']) or ('Cafe' in new[i]['businesses'][j]['name']):
            cafe += 1
        if ('Pubs' in new[i]['businesses'][j]['categories']) or ('Bar' in new[i]['businesses'][j]['name']):
            pub += 1
    loc['#cafes'] = cafe
    loc['#pubs'] = pub
    
    analysis.append(loc)

summary = json.dumps(analysis)
with open('yelp_clean2.json', 'w') as d:
    json.dump(summary, d)

# convert to CSV
x = json.loads(summary)
f = csv.writer(open("yelp.csv", "wb+"))
f.writerow(['latitude', 'longitude', 'avg_rating', '#cafes', '#pubs'])

for x in x:
    f.writerow([x['latitude'], 
                x['longitude'], 
                x['avg_rating'], 
                x['#cafes'],
                x['#pubs']])