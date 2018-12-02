import collections
import json
import threading
import time
import queue
import multiprocessing

from portfolio import *
from dbManager import dbManager
from sqlalchemy import desc
from decimal import Decimal

class CheckableQueue():  # or OrderedSetQueue
  def __init__(self, source_queue):
    self.source_queue = source_queue
  def __contains__(self, item):
    e = None
    res = False
    tmp = queue.Queue()
    #with self.source_queue.mutex:
    while len(self.source_queue.queue):
      e = self.source_queue.get_nowait()
      if e == item:
        res = True
      tmp.put(e)
    while not tmp.empty():
      self.source_queue.put(tmp.get())
    return res


def createPath(node, oldPath):
  path = list()
  if oldPath:
    path = oldPath.split('-')
  visited = list()
  res = ""
  while node and not visited.count(node):
    visited.append(node)
    path.append(str((node.restId)).lower().strip())
    node = node.parent
  path.sort()
  path.reverse()
  if path:
    res = path.pop()
  while path:
    res += '-' + path.pop()
  return res

def addPortfolio(portfolio, assetString):
  assetList = assetString.split('-')
  for asset in assetList:
    portfolio.addAsset(asset, 100)

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

  def sharpeTree(self, assetList, path, pathList, height):
    maxSharpe = Decimal(0.0)
    copySelf = self.deepCopy()
    path = createPath(self, None)
    portfolio = Portfolio()
    addPortfolio(portfolio, path)

# REMOVE ME
    toto = self
    prof = 0
    while toto :
      prof = prof + 1
      toto = toto.parent
    print(prof)
###########

    tmp = list()
    for a in assetList:
      if not (a == self):
        tmp.append(a.deepCopy())
    for asset in tmp:
      maxSharpe = max(maxSharpe, asset.sharpe)
      # Elagage sharpe
      if (Decimal(asset.sharpe) > Decimal(maxSharpe) / Decimal(1.18)) and (abs(portfolio.getCorrelation(asset.restId)) < 0.35):
        asset.parent = copySelf
        # Elagage unicité
        if (not pathList.count(createPath(asset, None))):
          copySelf.childrens.append(asset)
          if (path.count('-') + 1 == height) and (not pathList.count(path)):
            pathList.append(path)
        else:
          asset.parent = None
          #print("Elagage unicité")
          continue
      # else:
        # print("Elagage sharpe | max children reach")
      if not copySelf.childrens:
        # print("path : " + path)
        if (path.count('-') + 1 == height) and (not pathList.count(path)):
          pathList.append(path)
    for children in copySelf.childrens:
      if (path.count('-') + 1 < height) and (len(pathList) < 120):
      # if (path.count('-') < height):
        children.sharpeTree(tmp, path, pathList, height)

  def sharpeTree2(self, assetList, path, pathList, height):
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
        if (not createPath(asset, None) in CheckableQueue(pathList)):
          copySelf.childrens.append(asset)
          if (path.count('-') + 1 == height) and (not path in CheckableQueue(pathList)):
            pathList.put_nowait(path)
        else:
          asset.parent = None
          #print("Elagage unicité")
          continue
      # else:
        # print("Elagage sharpe")
      if not copySelf.childrens:
        # print("path : " + path)
        if (path.count('-') + 1 == height) and (not pathList.count(path)):
          pathList.put_nowait(path)
    for children in copySelf.childrens:
      if (path.count('-') + 1 < height):
        children.sharpeTree2(tmp, path, pathList, height)

def worker(a, assetList, threadpathList, height):
  a.sharpeTree2(assetList, "", threadPathList, height)
  print(threadpathList)

if __name__ == "__main__":

  assetList = list()
  db = dbManager()
  query = db.getAssets().order_by(desc('sharpe')).all()
  for asset in query:
    tmp = nodeAsset(asset.rest_id, asset.close_value + (asset.close_value_decimal / 1000000000000) - 1,
                    asset.asset_type, asset.sharpe)
    assetList.append(tmp)
  db.close()

  pathList = list()
  threadPathList = queue.Queue()

  start = time.time()
  assetList[0].sharpeTree(assetList, "", pathList, 20)
  end = time.time()
  print(end - start)
  print(len(pathList))

  start = time.time()

  portfolioList = []
  maxSharpe = 0
  for assetString in pathList:
    portfolio = Portfolio()
    addPortfolio(portfolio, assetString)
    portfolio.put()
    portfolio.computeSharpe()
    portfolioList.append(portfolio, portfolio.getSharpe())
    print("Assets : ", assetString, ". Sharpe : ", portfolio.getSharpe())
  print(end - start)
  
  sorted(portfolioList, key=lambda x: x[1])

  # start = time.time()
  # jobs = []
  # for i in range(5):
  #   p = multiprocessing.Process(target=worker, args=(assetList[i], assetList, threadPathList, 3,))
  #   p.start()
  #   jobs.append(p)
  # end = time.time()
  # print(end - start)

  # i = 0
  # threadPathList.put("toto")
  # print(threadPathList.empty())
  # while not threadPathList.empty():
  #   a = threadPathList.get()
  #   print(a)
  #   print(threadPathList.empty())
  # print("out")
