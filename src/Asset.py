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
		if (asset["TYPE"]["value"] == "PORTFOLIO" or asset["FIRST_QUOTE_DATE"]["value"] != "2012-01-02"):
			continue
		assetId = int(asset["REST_OBJECT_ID"]["value"])
		response = api.get('asset/'+ str(assetId) + '/quote')
		quote = json.loads(response)
		price = getPrice(quote[0]["nav"]["value"], acm.changeRate, asset["CURRENCY"]["value"])
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
	data = {"ratio": [20], "asset": [assetId], "start_date": "2012-01-02", "end_date": "2018-08-31"}
	api = RestManager()
	response = api.post("ratio/invoke", data)
	res = json.loads(response)
	return float((res[str(assetId)]["20"]["value"]).replace(',', '.'))

def getAssetValue(assetId):
	db = dbManager()
	ass = db.getAsset(assetId)
	return ass.close_value + (ass.close_value_decimal / 1000000000000) - 1

def getAssetType(assetId):
	db = dbManager()
	ass = db.getAsset(assetId)
	return ass.asset_type

if __name__ == "__main__":
	getAssets()