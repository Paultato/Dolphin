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

  def breadthTraversal(self):
      q = collections.deque()
      visited = collections.deque()
      pathList = list()
      q.append(self)
      q.append(None)

      size = 1
      maxRow = 0
      while size:
          node = q.popleft()
          path = createPath(node, None)
          size -= 1
          if node:
              if not visited.count(node) and (path not in pathList):
                  visited.append(node)
                  print("node : " + str(node.value), "parent : " +
                        str(node.parent), "path : " + path, sep=' -  *  - ')
                  i = 0
                  while i < len(node.childrens):
                      data = json.loads(node.childrens[i].value)['sharpe']
                      maxRow = max(maxRow, data)
                      i += 1

                  i = 0
                  j = 0
                  while i < len(node.childrens):
                      if json.loads(node.childrens[i].value)['sharpe'] >= maxRow / 1.5:
                          node.childrens[i].setParent(node)
                          q.append(node.childrens[i])
                          j += 1
                      i += 1
                  size += j
                  pathList.append(path)

          else:
              print("—")
              q.append(None)
              size += 1
              maxRow = 0

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
    print("parent : " + str(copySelf.restId))
    for asset in tmp:
      maxSharpe = max(maxSharpe, asset.sharpe)
      # Elagage sharpe
      if (Decimal(asset.sharpe) > Decimal(maxSharpe) / Decimal(1.5)):   
        asset.parent = copySelf
        # Elagage unicité
        if (not pathList.count(createPath(asset, None))):
          copySelf.childrens.append(asset)
        else:
          asset.parent = None
          print("Elagage unicité")
          continue
      else:
        print("Elagage sharpe")
      # FixMe : Not sure if path is added after removed from unicity constrain
      # Paths added and seem ok to me, need double check
      if not copySelf.childrens:
        print("path : " + path)
        if not pathList.count(path):
          pathList.append(path)
    for children in copySelf.childrens:
      children.sharpeTree(tmp, path, pathList)


if __name__ == "__main__":

  assetList = list()
  db = dbManager()
  query = db.getAssets().order_by(desc('sharpe')).limit(10).all()
  for asset in query:
    tmp = nodeAsset(asset.rest_id, asset.close_value + (asset.close_value_decimal / 1000000000000) - 1,
                    asset.asset_type, asset.sharpe)
    assetList.append(tmp)
  db.close()

  # root = Node(json.dumps({'name': "A", 'sharpe': 0.6}))
  # n1 = Node(json.dumps({'name': "B", 'sharpe': 0.5}))
  # n2 = Node(json.dumps({'name': "C", 'sharpe': 0.4}))
  # n3 = Node(json.dumps({'name': "D", 'sharpe': 0.2}))
  # n4 = Node(json.dumps({'name': "E", 'sharpe': 0.7}))
  # n5 = Node(json.dumps({'name': "F", 'sharpe': 0.6}))
  # n6 = Node(json.dumps({'name': "G", 'sharpe': 0.5}))
  # n7 = Node(json.dumps({'name': "H", 'sharpe': 0.4}))
  # n8 = Node(json.dumps({'name': "I", 'sharpe': 0.1}))
  # n9 = Node(json.dumps({'name': "J", 'sharpe': 0.1}))

  # root.setChildrens([n1, n2, n3])
  # n1.setChildrens([n4, n5])
  # n2.setChildrens([n6, n7, n3, n8, root])
  # n3.setChildrens([n8, n9, n2])

  # root.breadthTraversal()
  pathList = list()
  a = assetList[0]
  a.sharpeTree(assetList, "", pathList)
  # a.prettyPrint()
  print(assetList)
