import dbManager
import json
from RestManager import RestManager

def getAssets():
	api = RestManager()
	response = api.get('asset')
	assets = json.loads(response)

	for asset in assets:
		price *= getPrice(asset["LAST_CLOSE_VALUE"]["value"])
		insert(asset["REST_OBJECT_ID"]["value"], price)


def getPrice(price_str):
	price_str = price[0:len(price_str) - 2]
	price = float(price_str)
	return price