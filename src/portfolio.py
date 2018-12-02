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

	def __init__(self):
		self.assets = []

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
		body = {"ratio": [20], "asset": [1034],
                    "start_date": "2012-01-02", "end_date": "2018-08-31"}
		response = api.post('ratio/invoke', body)
		res = json.loads(response)
		self.sharpe = res["1034"]["20"]["value"]

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
		self.assets.append((asset, quantity, 0, '')) 

	def computeValues(self):
		new = []
		for a in self.assets:
			new.append((a[0], a[1], Asset.getAssetValue(a[0])))
		self.assets = new

	def computeTypes(self):
		new = []
		for a in self.assets:
			new.append((a[0], a[1], a[2], Asset.getAssetType(a[0])))
		self.assets = new

	def dump(self):
		total = 0
		qtt = 0
		for asset in self.assets:
			total += asset[1] * asset[2]
			qtt += asset[1]
		for pair in self.assets:
			print(pair[0], ' : ', pair[1], ' -> ', pair[1] * pair[2], " : ", pair[1] * pair[2] / total * 100, " type : ", pair[3])
		print("Total : ", total)
		print("Fund : ", self.getTypeRep())


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

	def getTypeRep(self):
		total = 0
		totFund = 0
		for a in self.assets:
			total += a[1] * a[2]
		for a in self.assets:
			if (a[3] == 'FUND'):
				totFund += a[1] * a[2]
		return totFund / total * 100

	def decrement(self, asset):
		for ass in self.assets:
			if (ass[0] == asset):
				self.assets.remove(ass)
				self.assets.append((ass[0], ass[1] - 1, ass[2], ass[3]))

	def increment(self, asset): 
		for ass in self.assets:
			if (ass[0] == asset):
				self.assets.remove(ass)
				self.assets.append((ass[0], ass[1] + 1, ass[2], ass[3]))

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
			if (len(more) > 0):
				self.decrement((self.max(more))[0])
			elif (len(less) > 0):
				self.increment((self.min(less))[0])
			nav = self.getNAV()
			more = nav[0]
			less = nav[1]
			print(nav)
		if (self.getTypeRep() > 50):
			self.decrement(self.getHigherFund())
			self.ponderate()

	def getHigherFund(self):
		high = (0, 0, 0, '')
		for a in self.assets:
			if (a[1] * a[2] > high[1] * high[2]):
				high = a
		return high[0]
	
if __name__ == "__main__":
	# Test portfolio ponderation
	pf = Portfolio()
	pf.addAsset(807, 100)
	pf.addAsset(717, 100)
	pf.addAsset(909, 100)
	pf.addAsset(873, 100)
	pf.addAsset(906, 100)
	pf.addAsset(743, 100)
	pf.addAsset(617, 100)
	pf.addAsset(885, 100)
	pf.addAsset(687, 100)
	pf.addAsset(1002, 100)
	pf.addAsset(792, 100)
	pf.addAsset(705, 100)
	pf.addAsset(813, 100)
	pf.addAsset(993, 100)
	pf.addAsset(877, 100)
	pf.addAsset(753, 100)
	pf.addAsset(686, 100)
	pf.addAsset(960, 100)
	pf.addAsset(944, 100)
	pf.addAsset(883, 100)
	pf.computeValues()
	pf.computeTypes()
	pf.ponderate()
	pf.dump()
	pf.put()
	pf.computeSharpe()

	print(pf.getSharpe())
	
	




