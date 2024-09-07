import numpy as np

from planeStressPackage.Node import Node
from planeStressPackage.Geometry import Geometry
from planeStressPackage.NodeList import NodeList
from planeStressPackage.Element import Element
from planeStressPackage.ElementList import ElementList
from planeStressPackage.Material import Material
from planeStressPackage.NumericalIntegration import NumericalIntegration
from planeStressPackage.Structure import Structure


class case2D:
    geometry = Geometry("mesh_box.csv")
    nodelist = NodeList(geometry)
    mat = Material(250, 0.3)
    ni = NumericalIntegration(3)
    elementlist = ElementList(mat, nodelist, ni)
    n1 = nodelist.getNode(0)
    e1 = elementlist.getElement(0)
    struct = Structure(nodelist, elementlist)
    struct.assembleLoadVector()
    struct.assembleStiffnessMatrix()
    # f1 = Force(10,20)
    # f2 = Force(20,20)
    # c1 = Constraint(False, False)
    # n1.setForce(f1)
    # n2 = nodelist.getNode(2)
    # n2.setForce(f2)
    # # print(nodelist.getNode(0).print())

    # element = Element(nodelist, mat, ni)
    # csr = element.computeStiffnessMatrix(1)
    # print(csr)
    # struct.solve()
    # struct.printResults()


