from planeStressPackage.Constraint import Constraint
from planeStressPackage.Force import Force
from planeStressPackage.Geometry import Geometry
from planeStressPackage.NodeList import NodeList
from planeStressPackage.Element import Element
from planeStressPackage.ElementList import ElementList
from planeStressPackage.Material import Material
from planeStressPackage.NumericalIntegration import NumericalIntegration
from planeStressPackage.Structure import Structure
from Visualizer import Visualizer


class Case2D:
    geometry = Geometry("mesh_rect.csv")
    nodelist = NodeList(geometry)
    mat = Material(10000, 0.3)
    ni = NumericalIntegration(3)
    elementlist = ElementList()
    f1 = Force(10, 0)
    fixed = Constraint(False, False)
    free = Constraint(True, True)
    y_fixed = Constraint(True, False)
    ele_1 = Element(nodelist, mat, ni=ni, height=1, case_type=0)
    ele_2 = Element(nodelist, mat, ni=ni, height=1, case_type=0)
    elementlist.setElement(ele_1)
    elementlist.setElement(ele_2)
    ele_1.setNode(0, nodelist.getNode(0))
    ele_1.setNode(1, nodelist.getNode(1))
    ele_1.setNode(2, nodelist.getNode(4))
    ele_1.setNode(3, nodelist.getNode(5))
    ele_2.setNode(0, nodelist.getNode(1))
    ele_2.setNode(1, nodelist.getNode(2))
    ele_2.setNode(2, nodelist.getNode(3))
    ele_2.setNode(3, nodelist.getNode(4))
    ele_1.getNode(0).setConstraint(fixed)
    ele_1.getNode(1).setConstraint(y_fixed)
    ele_1.getNode(2).setConstraint(y_fixed)
    ele_1.getNode(3).setConstraint(fixed)
    ele_2.getNode(0).setConstraint(y_fixed)
    ele_2.getNode(1).setConstraint(free)
    ele_2.getNode(2).setConstraint(free)
    ele_2.getNode(3).setConstraint(y_fixed)
    ele_2.getNode(1).setForce(f1)
    ele_2.getNode(2).setForce(f1)
    c2 = ele_2.enumerateDOFs()
    c1 = ele_1.enumerateDOFs()
    print(c1, c2)
    # struct = Structure(nodelist, elementlist)
    # struct.solve()
    # struct.printResults()
    # v = Visualizer(struct)
    # v.drawElements(0.5)
    # v.drawConstraints()
    # v.drawForces()
    # v.drawDeformed(0.5)
    # v.plotAll()
