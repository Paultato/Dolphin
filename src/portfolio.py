import json
from RestManager import RestManager

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

	def getSharpe(self):
		api = RestManager()
		body = {"ratio": [20], "asset": [1034]}
		response = api.post('ratio/invoke', body)
		res = json.loads(response)
		return res["1034"]["20"]["value"]

	def addAsset(self, asset, quantity):
		self.assets.append((asset, quantity)) 

	def dump(self):
		for pair in self.assets:
			print(pair[0], ' : ', pair[1])


