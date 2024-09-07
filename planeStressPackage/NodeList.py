import numpy as np

from planeStressPackage.Node import Node
from planeStressPackage.Geometry import Geometry


class NodeList:
    def __init__(self, geom: Geometry):
        self.Geometry = geom
        self.nodeList = np.array([Node(self.Geometry.getPoint(0)[0], self.Geometry.getPoint(0)[1]),
                                  Node(self.Geometry.getPoint(1)[0], self.Geometry.getPoint(1)[1]),
                                  Node(self.Geometry.getPoint(2)[0], self.Geometry.getPoint(2)[1]),
                                  Node(self.Geometry.getPoint(3)[0], self.Geometry.getPoint(3)[1]),
                                  ])

    def getNode(self, idx: int):
        return self.nodeList[idx]

    def setNode(self, idx: int, node: Node):
        self.nodeList[idx] = node

    def get_NumberOfNodes(self):
        return len(self.nodeList)
