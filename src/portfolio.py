import json
import Asset
from dbManager import dbManager
from RestManager import RestManager
from correlation import CorrelationManager

class Portfolio:
	assets = []
	sharpe = 0

	label = "epita_group_7"
	code = "EUR"
	typef = "front"
	date = "2012-01-02"

	def buildJson(self):
		assetList = []
		for pair in self.assets:
			assetList.append({'asset': {'asset': pair[0], 'quantity': pair[1]}})
		return {'currency': {'code': self.code}, 'label': self.label, 'type': self.typef, 'values': {self.date: assetList}}

	def put(self):
		api = RestManager()
		body = self.buildJson()
		api.put('portfolio/1034/dyn_amount_compo', body)

	def computeSharpe(self):
		api = RestManager()
		body = {"ratio": [20], "asset": [1034]}
		response = api.post('ratio/invoke', body)
		res = json.loads(response)
		self.sarpe = res["1034"]["20"]["value"]

	def getSharpe(self):
		return self.sharpe

	def getCorrelation(self, asset):
		cm = CorrelationManager()
		cm.build_df()
		tot = 0
		for cur in self.assets:
			correl = cm.value(asset, cur[0])
			tot += float(correl.replace(',', '.'))
		return tot / len(self.assets)

	def addAsset(self, asset, quantity):
		self.assets.append((asset, quantity, Asset.getAssetValue(asset))) 

	def dump(self):
		for pair in self.assets:
			print(pair[0], ' : ', pair[1], ' -> ', pair[1] * pair[2])

	def getNAV(self):
			total = 0
			more = []
			less = []
			for asset in self.assets:
				total += asset[1] * asset[2]
			for asset in self.assets:
				sup = total / 10
				und = total / 100
				value = asset[1] * asset[2]
				if (value > sup):
					more.append((asset[0], asset[1], value/total))
				if (value < und):
					less.append((asset[0], asset[1], value/total))
			return (more, less)

pf = Portfolio()
pf.addAsset(1001, 10)
pf.addAsset(687, 1)
print(pf.getNAV())