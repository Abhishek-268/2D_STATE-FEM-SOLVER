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
    geometry = Geometry("mesh_box.csv")
    nodelist = NodeList(geometry)
    mat = Material(10000, 0.3)
    ni = NumericalIntegration(3)
    elementlist = ElementList()
    f1 = Force(10, 0)
    fixed = Constraint(False, False)
    free = Constraint(True, True)
    ele = Element(nodelist, mat, ni, 0.1)
    elementlist.setElement(ele)
    ele.getNode1().setConstraint(fixed)
    ele.getNode2().setConstraint(free)
    ele.getNode3().setConstraint(free)
    ele.getNode4().setConstraint(fixed)
    ele.getNode2().setForce(f1)
    ele.getNode3().setForce(f1)
    struct = Structure(nodelist, elementlist)
    struct.solve()
    struct.printResults()
    v = Visualizer(struct)
    v.drawElements(0.5)
    v.drawConstraints()
    v.drawForces()
    v.drawDeformed(0.5)
    v.plotAll()
