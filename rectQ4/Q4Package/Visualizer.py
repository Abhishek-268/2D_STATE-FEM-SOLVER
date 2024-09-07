import pyvista as pv
import numpy as np

from PyPlus.Structure import Structure


class Visualizer:

    def __init__(self, struct: Structure):
        self.displacementscale = 0.0
        self.symbolscale = 0.0
        self.structure = struct
        self.plot = pv.Plotter()

    def drawElements(self):
        # Create a PolyData object
        for element in self.structure.elementList:
            truss = pv.Line(pointa=element.getNode1().getPosition(), pointb=element.getNode2().getPosition())
            # Create a plotter object
            # Display the plot
            self.plot.add_mesh(truss, color='lightblue', show_edges=True)

    def drawConstraints(self):
        for node in self.structure.nodeList:
            for i in range(3):
                dirC = node.getConstraint().isFree(i)
                # print("dirC ",dirC)
                if not dirC:
                    if i == 0:
                        cone1 = pv.Cone(center=node.position, radius=0.3, height=0.8, direction=[-1.0, 0.0, 0.0])
                        self.plot.add_mesh(cone1)
                    if i == 1:
                        cone2 = pv.Cone(center=node.position, radius=0.3, height=0.8, direction=[0.0, -1.0, 0.0])
                        self.plot.add_mesh(cone2)

                    if i == 2:
                        cone3 = pv.Cone(center=node.position, radius=0.3, height=0.8, direction=[0.0, 0.0, -1.0])
                        self.plot.add_mesh(cone3)

    def drawForces(self):
        self.symbolscale = 0.5
        for node in self.structure.nodeList:
            if node.force.getComponents(0) != 0:
                force = pv.Arrow(start=node.getPosition(), direction=[-1.0, 0.0, 0.0])
                self.plot.add_mesh(force)

            if node.force.getComponents(1) != 0:
                force = pv.Arrow(start=node.getPosition(), direction=[0.0, -1.0, 0.0])
                self.plot.add_mesh(force)

            if node.force.getComponents(2) != 0:
                force = pv.Arrow(start=node.getPosition(), direction=[0.0, 0.0, -1.0])
                self.plot.add_mesh(force)

    def drawDeformed(self, scale: int):
        for element in self.structure.elementList:
            pos1 = np.array(element.getNode1().getPosition()) + scale * np.array(element.getNode1().getDisplacement())
            pos2 = np.array(element.getNode2().getPosition()) + scale * np.array(element.getNode2().getDisplacement())
            truss = pv.Line(pointa=pos1, pointb=pos2)
            # Create a plotter object
            # Display the plot
            self.plot.add_mesh(truss, color='red', show_edges=True)

    @staticmethod
    def plotAll(self):
        self.plot.show()
