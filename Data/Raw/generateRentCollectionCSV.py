import csv
import json
from datetime import datetime
import time 

"""
	Use rentCollectionData.json to generate a CSV that has the following fields:
	address, price, move-in timestamp, move-in date, bedrooms
"""

def genTotalCSV(jsonFile):
	with open(jsonFile, 'r') as raw_rent:
		rent_json = json.load(raw_rent)
	with open('rent_collection_board.csv', 'w') as rent_csv:
		csv_writer = csv.DictWriter(rent_csv, fieldnames=['address', 'price', 'movein_t', 'movein_d', 'bedrooms'])
		csv_writer.writeheader()
		for building in rent_json['housing']:
			address = building['number'] + " " + building['name']
			for unit in [key for key in building.keys() if key.isdigit()]:
				write_dict = {
					"address": address,
					"movein_d": building[unit]['started'],
					"movein_t": time.mktime(datetime.strptime(building[unit]['started'], "%Y-%m-%d").timetuple()),
					"price": building[unit]['price'],
					"bedrooms": building[unit]['bedrooms']
				}
				csv_writer.writerow(write_dict)

def genAverageCSV(jsonFile):
	with open(jsonFile, 'r') as raw_rent:
		rent_json = json.load(raw_rent)
	with open('rent_collection_board_avg_ppr.csv', 'w') as rent_csv:
		csv_writer = csv.DictWriter(rent_csv, fieldnames=['address', 'avg_ppr'])
		csv_writer.writeheader()
		for building in rent_json['housing']:
			address = building['number'] + " " + building['name']
			avg_ppr = []
			for unit in [key for key in building.keys() if key.isdigit()]:
				dividend = building[unit]['bedrooms'] if building[unit]['bedrooms'] > 0 else 1
				avg_ppr += [float(building[unit]['price'])/dividend]
			write_dict = {
				"address": address,
				"avg_ppr": float(sum(avg_ppr))/len(avg_ppr)
			}
			csv_writer.writerow(write_dict)

if __name__ == "__main__":
	genTotalCSV('rentCollectionData.json')
	genAverageCSV('rentCollectionData.json')
