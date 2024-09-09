from quadElement_FEM.Constraint import Constraint
from quadElement_FEM.Force import Force
from quadElement_FEM.Geometry import Geometry
from quadElement_FEM.NodeList import NodeList
from quadElement_FEM.Element import Element
from quadElement_FEM.ElementList import ElementList
from quadElement_FEM.Material import Material
from quadElement_FEM.NumericalIntegration import NumericalIntegration
from quadElement_FEM.Structure import Structure
from quadElement_FEM.Visualizer import Visualizer
class Case2DTest2:
    geometry = Geometry("mesh_skewed_quad.csv")
    nodelist = NodeList(geometry)
    mat = Material(15000, 0.25)
    ni = NumericalIntegration(3)
    elementlist = ElementList()
    f2 = Force(15, 5)
    fixed = Constraint(False, False)
    free = Constraint(True, True)
    y_fixed = Constraint(True, False)

    # Define two quadrilateral elements
    ele_1 = Element(nodelist, mat, ni=ni, height=1.5, case_type=0)
    ele_2 = Element(nodelist, mat, ni=ni, height=1.5, case_type=0)
    elementlist.setElement(ele_1)
    elementlist.setElement(ele_2)

    # Set nodes for the elements
    ele_1.setNode(0, nodelist.getNode(0))  # Fixed node
    ele_1.setNode(1, nodelist.getNode(1))  # Constrained in y, free in x
    ele_1.setNode(2, nodelist.getNode(4))  # Free node
    ele_1.setNode(3, nodelist.getNode(5))  # Fixed node

    ele_2.setNode(0, nodelist.getNode(1))  # Constrained in y, free in x
    ele_2.setNode(1, nodelist.getNode(2))  # Free node
    ele_2.setNode(2, nodelist.getNode(3))  # Free node
    ele_2.setNode(3, nodelist.getNode(4))  # Free node

    # Apply constraints and forces
    ele_1.getNode(0).setConstraint(fixed)
    ele_1.getNode(3).setConstraint(fixed)
    ele_1.getNode(1).setConstraint(y_fixed)
    ele_1.getNode(2).setConstraint(free)
    ele_2.getNode(1).setConstraint(free)
    ele_2.getNode(2).setConstraint(free)
    ele_2.getNode(1).setForce(f2)
    ele_2.getNode(2).setForce(f2)

    struct = Structure(nodelist, elementlist)
    struct.solve("connections_skewed_quad.csv")
    struct.printResults()
    v = Visualizer(struct)
    v.drawElements(0.5)
    v.drawConstraints()
    v.drawForces()
    v.drawDeformed(0.5)
    v.plotAll()
