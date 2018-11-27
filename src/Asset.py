from dbManager import dbManager
import json
import math
from RestManager import RestManager
from currencyManager import AssetCurrencyManager

def getAssets():
	api = RestManager()
	db = dbManager()
	response = api.get('asset')
	assets = json.loads(response)
	acm = AssetCurrencyManager()

	for asset in assets:
		if (asset["TYPE"]["value"] == "PORTFOLIO"):
			continue
		assetId = int(asset["REST_OBJECT_ID"]["value"])
		price = getPrice(asset["LAST_CLOSE_VALUE"]["value"], acm.changeRate, asset["CURRENCY"]["value"])
		sharpe = getSharpe(assetId)
		price = splitPrice(price)
		db.insertAsset(assetId, price[0], price[1], asset["TYPE"]["value"], sharpe)

def splitPrice(floatPrice):
	split = math.modf(floatPrice)
	price = (int(split[1]), int(split[0] * 1000000000000) + 1000000000000)
	return price

def getPrice(price_str, changeRate, currency):
	price_str = price_str.replace(',', '.')
	price_str = price_str.split(' ', 1)[0]
	price = float(price_str)
	price *= float(changeRate[currency])
	return price

def getSharpe(assetId):
	data = {"ratio": [20], "asset": [assetId]}
	api = RestManager()
	response = api.post("ratio/invoke", data)
	res = json.loads(response)
	return float((res[str(assetId)]["20"]["value"]).replace(',', '.'))

getAssets()