import numpy as np

from planeStressPackage.Node import Node
from planeStressPackage.Geometry import Geometry


class NodeList:
    def __init__(self, geom: Geometry):
        self.Geometry = geom
        self.nodeList = []
        for i in range(len(geom.pointList)):
            self.nodeList.append(Node(geom.pointList[i][0], geom.pointList[i][1]))


    def getNode(self, idx: int):
        return self.nodeList[idx]

    def setNode(self, idx: int, node: Node):
        self.nodeList[idx] = node

    def get_NumberOfNodes(self):
        return len(self.nodeList)


