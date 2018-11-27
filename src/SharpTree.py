import collections
import json
from dbManager import *


def createPath(node):
  path = list()
  res = ""
  while node:
    ##path.append("".join(sorted((json.loads(node.value)['name'].lower()))).strip())
    path.append(json.loads(node.value)['name'].lower().strip())
    node = node.parent
  path.sort()
  path.reverse()
  if path:
    res = path.pop()
  while path:
    res += '-' + path.pop()
  return res

class Node:
  def __init__(self, value, parent=[], childrens=[]):
    self.value = value
    self.parent = parent
    self.childrens = childrens

  def setParent(self, parent):
    self.parent = parent

  def setChildrens(self, childrens):
    self.childrens = childrens

  def __str__(self):
    return str(json.loads(self.value))

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
      path = createPath(node)
      size -= 1
      if node :
        if not visited.count(node) and (path not in pathList) :
          visited.append(node)
          print("node : " + str(node.value), "parent : " + str(node.parent), "path : " + path, sep=' -  *  - ')
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


      
if __name__ == "__main__":

  db = dbManager()
  query = db.getAssets()
  print(query)
  db.close()
  
  root = Node(json.dumps({'name': "45", 'sharpe': 0.6}))
  n1 = Node(json.dumps({'name': "74", 'sharpe': 0.5}))
  n2 = Node(json.dumps({'name': "13", 'sharpe': 0.4}))
  n3 = Node(json.dumps({'name': "99", 'sharpe': 0.2}))
  n4 = Node(json.dumps({'name': "13", 'sharpe': 0.7}))
  n5 = Node(json.dumps({'name': "99", 'sharpe': 0.6}))
  n6 = Node(json.dumps({'name': "74", 'sharpe': 0.5}))
  n7 = Node(json.dumps({'name': "99", 'sharpe': 0.4}))
  n8 = Node(json.dumps({'name': "74", 'sharpe': 0.1}))
  n9 = Node(json.dumps({'name': "13", 'sharpe': 0.1}))

  root.setChildrens([n1, n2, n3])
  n1.setChildrens([n4, n5])
  n2.setChildrens([n6, n7])
  n3.setChildrens([n8, n9])

  root.breadthTraversal()


