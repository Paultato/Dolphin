import collections
import json
from dbManager import *
from sqlalchemy import desc
from decimal import Decimal


def createPath(node, oldPath):
  path = list()
  if oldPath:
    path = oldPath.split('-')
  visited = list()
  res = ""
  while node and not visited.count(node):
    visited.append(node)
    # path.append("".join(sorted((json.loads(node.value)['name'].lower()))).strip())
    path.append(str((node.restId)).lower().strip())
    node = node.parent
  path.sort()
  path.reverse()
  if path:
    res = path.pop()
  while path:
    res += '-' + path.pop()
  return res


class nodeAsset:
  def __init__(self, restId, closeValue, type, sharpe):
    self.restId = restId
    self.closeValue = closeValue
    self.type = type
    self.sharpe = sharpe
    self.parent = None
    self.childrens = list()

  def deepCopy(self):
    tmp = nodeAsset(0, 0, 0, 0)
    tmp.restId = self.restId
    tmp.closeValue = self.closeValue
    tmp.type = self.type
    tmp.sharpe = self.sharpe
    tmp.parent = self.parent
    tmp.childrens = list()
    return tmp

  def prettyPrint(self):
      createPath(self, None)

  def sharpeTree(self, assetList, path, pathList):
    maxSharpe = Decimal(0.0)
    copySelf = self.deepCopy()
    path = createPath(self, None)
    tmp = list()
    for a in assetList:
      if not (a == self):
        tmp.append(a.deepCopy())
    for asset in tmp:
      maxSharpe = max(maxSharpe, asset.sharpe)
      # Elagage sharpe
      if (Decimal(asset.sharpe) > Decimal(maxSharpe) / Decimal(1.2)):   
        asset.parent = copySelf
        # Elagage unicité
        if (not pathList.count(createPath(asset, None))):
          copySelf.childrens.append(asset)
          if (path.count('-') + 1 == 20) and (not pathList.count(path)):
            pathList.append(path)
        else:
          asset.parent = None
          print("Elagage unicité")
          continue
      else:
        print("Elagage sharpe")
      if not copySelf.childrens:
        print("path : " + path)
        if (path.count('-') + 1 == 20) and (not pathList.count(path)):
          pathList.append(path)
    for children in copySelf.childrens:
      if (path.count('-') + 1 < 20):
        children.sharpeTree(tmp, path, pathList)


if __name__ == "__main__":

  assetList = list()
  db = dbManager()
  query = db.getAssets().order_by(desc('sharpe')).limit(30).all()
  for asset in query:
    tmp = nodeAsset(asset.rest_id, asset.close_value + (asset.close_value_decimal / 1000000000000) - 1,
                    asset.asset_type, asset.sharpe)
    assetList.append(tmp)
  db.close()

  pathList = list()
  a = assetList[0]
  a.sharpeTree(assetList, "", pathList)
  for p in pathList:
    print(p)
