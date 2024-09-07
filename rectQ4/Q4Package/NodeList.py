import numpy as np

from Q4Package.Node import Node
from Q4Package.Geometry import Geometry


class NodeList:
    def __init__(self, geom: Geometry):
        self.a = 0
        self.b = 0
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

    def get_a(self):
        self.a = np.abs(self.getNode(2).getPosition()[1]-self.getNode(1).getPosition()[1])
        return self.a

    def set_a(self, val: float):
        self.a = val

    def get_b(self):
        self.b = np.abs(self.getNode(1).getPosition()[0] - self.getNode(0).getPosition()[0])
        return self.b










