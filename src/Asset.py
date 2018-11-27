from dbManager import dbManager
import json
from RestManager import RestManager

def getAssets():
	api = RestManager()
	db = dbManager()
	response = api.get('asset')
	assets = json.loads(response)

	for asset in assets:
		assetId = int(asset["REST_OBJECT_ID"]["value"])
		price = getPrice(asset["LAST_CLOSE_VALUE"]["value"])
		sharpe = getSharpe(assetId)
		db.insertAsset(assetId, price, asset["TYPE"]["value"], sharpe)


def getPrice(price_str):
	price_str = price_str.replace(',', '.')
	price_str = price_str[0:len(price_str) - 2]
	price = float(price_str)
	# TODO: conversion rate
	return price

def getSharpe(assetId):
	data ={"ratio": [20], "asset": [assetId]}
	api = RestManager()
	response = api.post("ratio/invoke", data)
	res = json.loads(response)
	return float(res[str(assetId)]["20"]["value"])

getAssets()