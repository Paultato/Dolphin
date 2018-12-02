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
		self.assets.append((asset, quantity, 0)) 

	def computeValues(self):
		new = []
		for a in self.assets:
			new.append((a[0], a[0], Asset.getAssetValue(a[0])))
		self.assets = new

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

	def decrement(self, asset):
		for ass in self.assets:
			if (ass[0] == asset):
				self.assets.remove(ass)
				self.assets.append((ass[0], ass[1] - 1, ass[2]))

	def increment(self, asset): 
		for ass in self.assets:
			if (ass[0] == asset):
				self.assets.remove(ass)
				self.assets.append((ass[0], ass[1] + 1, ass[2]))

	def max(self, assetList):
		max = (0, 0, 0)
		for asset in assetList:
			if (asset[2] > max[2]):
				max = asset
		return max

	def min(self, assetList):
		min = (0, 0, 1)
		for asset in assetList:
			if (asset[2] < min[2]):
				min = asset
		return min

	def ponderate(self):
		nav = self.getNAV()
		more = nav[0]
		less = nav[1]
		while (len(more) > 0 or len(less) > 0):
			if (len(more) > 0 and len(less) > 0):
				self.decrement((self.max(more))[0])
				self.increment((self.min(less))[0])
			elif (len(more) > 0):
				self.decrement((self.max(more))[0])
			elif (len(less) > 0):
				self.increment((self.min(less))[0])
			nav = self.getNAV()
			more = nav[0]
			less = nav[1]
			print(nav)
	
if __name__ == "__main__":
	# Test portfolio ponderation
	pf = Portfolio()
	pf.addAsset(933, 10)
	pf.addAsset(666, 10)
	pf.addAsset(944, 10)
	pf.addAsset(951, 10)
	#pf.addAsset(1016, 10)
	#pf.addAsset(1007, 10)
	#pf.addAsset(995, 10)
	#pf.addAsset(1005, 10)
	#pf.addAsset(1021, 10)
	#pf.addAsset(949, 10)
	#pf.addAsset(996, 10)
	#pf.addAsset(1006, 10)
	#pf.addAsset(960, 10)
	#pf.addAsset(912, 10)
	#pf.addAsset(774, 10)
	#pf.addAsset(978, 10)
	#pf.addAsset(663, 10)
	#pf.addAsset(733, 10)
	#pf.addAsset(781, 10)
	#pf.addAsset(1001, 10)
	#pf.dump()
	#print(pf.getNAV())
	#pf.ponderate()
	pf.dump()
	pf.computeValues()
	pf.dump()
	




