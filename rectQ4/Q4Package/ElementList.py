import numpy as np

from planeStressPackage.Element import Element
from planeStressPackage.Geometry import Geometry
from planeStressPackage.NodeList import NodeList
from planeStressPackage.Material import Material
from planeStressPackage.NumericalIntegration import NumericalIntegration


class ElementList:
    def __init__(self, mat: Material, nodelist: NodeList, ni: NumericalIntegration):
        self.ElementList = np.empty(nodelist.get_NumberOfNodes(), dtype=Element)
        for i in range(nodelist.get_NumberOfNodes()):
            self.ElementList[i] = Element(nodelist, mat, ni)

    def getElement(self, idx: int):
        return self.ElementList[idx]

    def setElement(self, idx: int, element: Element):
        self.ElementList[idx] = element

    def get_NumberOfElements(self):
        return len(self.ElementList)
