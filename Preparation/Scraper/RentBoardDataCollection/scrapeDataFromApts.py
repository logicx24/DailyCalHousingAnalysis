import requests
import glob
import json

addressesFile = glob.glob("../../Data/Clean/addresses.json")[0]


def doTheThings(addressesFilename):
	lem = []
	jdict = json.loads(open(addressesFilename).read())
	for address in jdict['addrs']:
		currstr = address[0] + "/" + address[1]
		res = requests.get("http://apartments.jerryuejio.com/map/br0123pr0-5000ls2014-01-01/api/address/" + currstr)
		lem.append(res.json())
	ret = {"housing": lem}
	with open('rentCollectionData.json', 'w') as out:
		json.dump(ret, out, indent=4)

doTheThings(addressesFile)
