import pyvista as pv
import numpy as np
from quadElement_FEM.Structure import Structure


class Visualizer:

    def __init__(self, struct: Structure):
        self.displacementscale = 0.0
        self.symbolscale = 0.1
        self.ele_length = None
        self.structure = struct
        self.plot = pv.Plotter()

    def drawElements(self, opacity: float):
        if opacity > 1:
            raise IndexError("Opacity greater than 1\nSet the value between 0 and 1")
        # Create a PolyData object
        for element in range(self.structure.elementlist.get_NumberOfElements()):
            self.ele_length = self.structure.elementlist.getElement(element).getLength()
            points = np.array([[self.structure.elementlist.getElement(element).getNode(0).getPosition()[0],
                                self.structure.elementlist.getElement(element).getNode(0).getPosition()[1],
                                0],
                               [self.structure.elementlist.getElement(element).getNode(1).getPosition()[0],
                                self.structure.elementlist.getElement(element).getNode(1).getPosition()[1],
                                0],
                               [self.structure.elementlist.getElement(element).getNode(2).getPosition()[0],
                                self.structure.elementlist.getElement(element).getNode(2).getPosition()[1],
                                0],
                               [self.structure.elementlist.getElement(element).getNode(3).getPosition()[0],
                                self.structure.elementlist.getElement(element).getNode(3).getPosition()[1],
                                0]
                               ])
            faces = np.array([4, 0, 1, 2, 3])
            quad = pv.PolyData(points, faces)
            self.plot.add_mesh(quad, color='purple', show_edges=True, opacity=opacity)
            self.plot.set_background("gray")

    def drawConstraints(self):
        for element in range(self.structure.elementlist.get_NumberOfElements()):
            self.ele_length = self.structure.elementlist.getElement(element).getLength()

        for j in range(self.structure.nodelist.get_NumberOfNodes()):
            for i in range(2):
                dirC = self.structure.nodelist.getNode(j).getConstraint().isFree(i)
                # print("dirC ",dirC)
                if not dirC:
                    if i == 0:
                        center = np.array([self.structure.nodelist.getNode(j).getPosition()[0],
                                           self.structure.nodelist.getNode(j).getPosition()[1],
                                           0
                                           ])
                        base_length = self.ele_length * self.symbolscale
                        height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle

                        # Define the triangle vertices (centered around the origin initially)
                        triangle_points = np.array([
                            [0, 0, 0],  # Top vertex
                            [-height, -base_length / 2, 0.0],  # Left vertex
                            [-height, base_length / 2, 0.0],  # Right vertex
                        ])

                        # Translate triangle to the center point

                        triangle_points += center

                        # Define the connectivity of the triangle
                        faces = np.array([[3, 0, 1, 2]])  # Single triangle face
                        triangle = pv.PolyData(triangle_points, faces)
                        self.plot.add_mesh(triangle, color='#000080', show_edges=True)
                    if i == 1:
                        center = np.array([self.structure.nodelist.getNode(j).getPosition()[0],
                                           self.structure.nodelist.getNode(j).getPosition()[1],
                                           0
                                           ])
                        base_length = self.ele_length * self.symbolscale
                        height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle

                        # Define the triangle vertices (centered around the origin initially)
                        triangle_points = np.array([
                            [0, 0, 0],
                            [-base_length / 2, -height, 0.0],  # Left vertex
                            [base_length / 2, -height, 0.0]  # Right vertex
                            # Top vertex
                        ])

                        # Translate triangle to the center point
                        triangle_points += center

                        # Define the connectivity of the triangle
                        faces = np.array([[3, 0, 1, 2]])  # Single triangle face
                        triangle = pv.PolyData(triangle_points, faces)
                        self.plot.add_mesh(triangle, color='#000080', show_edges=True)

            # for i in range(2):
            #     dirC = self.structure.elementlist.getElement(element).getNode(1).getConstraint().isFree(i)
            #     # print("dirC ",dirC)
            #     if not dirC:
            #         if i == 0:
            #             center = np.array([self.structure.elementlist.getElement(element).getNode(1).getPosition()[0],
            #                                self.structure.elementlist.getElement(element).getNode(1).getPosition()[1],
            #                                0
            #                                ])
            #             base_length = self.ele_length * self.symbolscale
            #             height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle
            #
            #             # Define the triangle vertices (centered around the origin initially)
            #             triangle_points = np.array([
            #                 [0, 0, 0],  # Top vertex
            #                 [height, -base_length / 2, 0.0],  # Left vertex
            #                 [height, base_length / 2, 0.0],  # Right vertex
            #             ])
            #
            #             # Translate triangle to the center point
            #
            #             triangle_points += center
            #
            #             # Define the connectivity of the triangle
            #             faces = np.array([[3, 0, 1, 2]])  # Single triangle face
            #             triangle = pv.PolyData(triangle_points, faces)
            #             self.plot.add_mesh(triangle, color='#000080', show_edges=True)
            #
            #         if i == 1:
            #             center = np.array([self.structure.elementlist.getElement(element).getNode(1).getPosition()[0],
            #                                self.structure.elementlist.getElement(element).getNode(1).getPosition()[1],
            #                                0
            #                                ])
            #             base_length = self.ele_length * self.symbolscale
            #             height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle
            #
            #             # Define the triangle vertices (centered around the origin initially)
            #             triangle_points = np.array([
            #                 [0, 0, 0],
            #                 [-base_length / 2, - height, 0.0],  # Left vertex
            #                 [base_length / 2, - height, 0.0]  # Right vertex
            #                 # Top vertex
            #             ])
            #
            #             # Translate triangle to the center point
            #             triangle_points -= center
            #
            #             # Define the connectivity of the triangle
            #             faces = np.array([[3, 0, 1, 2]])  # Single triangle face
            #             triangle = pv.PolyData(triangle_points, faces)
            #             self.plot.add_mesh(triangle, color='#000080', show_edges=True)
            #
            # for i in range(2):
            #     dirC = self.structure.elementlist.getElement(element).getNode(2).getConstraint().isFree(i)
            #     # print("dirC ",dirC)
            #     if not dirC:
            #         if i == 0:
            #             center = np.array([self.structure.elementlist.getElement(element).getNode(2).getPosition()[0],
            #                                self.structure.elementlist.getElement(element).getNode(2).getPosition()[1],
            #                                0
            #                                ])
            #             base_length = self.ele_length * self.symbolscale
            #             height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle
            #
            #             # Define the triangle vertices (centered around the origin initially)
            #             triangle_points = np.array([
            #                 [0, 0, 0],  # Top vertex
            #                 [-height, -base_length / 2, 0.0],  # Left vertex
            #                 [-height, base_length / 2, 0.0],  # Right vertex
            #             ])
            #
            #             # Translate triangle to the center point
            #
            #             triangle_points += center
            #
            #             # Define the connectivity of the triangle
            #             faces = np.array([[3, 0, 1, 2]])  # Single triangle face
            #             triangle = pv.PolyData(triangle_points, faces)
            #             self.plot.add_mesh(triangle, color='#000080', show_edges=True)
            #         if i == 1:
            #             center = np.array([self.structure.elementlist.getElement(element).getNode(2).getPosition()[0],
            #                                self.structure.elementlist.getElement(element).getNode(2).getPosition()[1],
            #                                0
            #                                ])
            #             base_length = self.ele_length * self.symbolscale
            #             height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle
            #
            #             # Define the triangle vertices (centered around the origin initially)
            #             triangle_points = np.array([
            #                 [0, 0, 0],
            #                 [-base_length / 2, height, 0.0],  # Left vertex
            #                 [base_length / 2, height, 0.0]  # Right vertex
            #                 # Top vertex
            #             ])
            #
            #             # Translate triangle to the center point
            #             triangle_points += center
            #
            #             # Define the connectivity of the triangle
            #             faces = np.array([[3, 0, 1, 2]])  # Single triangle face
            #             triangle = pv.PolyData(triangle_points, faces)
            #             self.plot.add_mesh(triangle, color='#000080', show_edges=True)
            #
            # for i in range(2):
            #     dirC = self.structure.elementlist.getElement(element).getNode(3).getConstraint().isFree(i)
            #     # print("dirC ",dirC)
            #     if not dirC:
            #         if i == 0:
            #             center = np.array([self.structure.elementlist.getElement(element).getNode(3).getPosition()[0],
            #                                self.structure.elementlist.getElement(element).getNode(3).getPosition()[1],
            #                                0
            #                                ])
            #             base_length = self.ele_length * self.symbolscale
            #             height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle
            #
            #             # Define the triangle vertices (centered around the origin initially)
            #             triangle_points = np.array([
            #                 [0, 0, 0],  # Top vertex
            #                 [-height, -base_length / 2, 0.0],  # Left vertex
            #                 [-height, base_length / 2, 0.0],  # Right vertex
            #             ])
            #
            #             # Translate triangle to the center point
            #
            #             triangle_points += center
            #
            #             # Define the connectivity of the triangle
            #             faces = np.array([[3, 0, 1, 2]])  # Single triangle face
            #             triangle = pv.PolyData(triangle_points, faces)
            #             self.plot.add_mesh(triangle, color='#000080', show_edges=True)
            #         if i == 1:
            #             center = np.array([self.structure.elementlist.getElement(element).getNode(3).getPosition()[0],
            #                                self.structure.elementlist.getElement(element).getNode(3).getPosition()[1],
            #                                0
            #                                ])
            #             base_length = self.ele_length * self.symbolscale
            #             height = base_length * np.sqrt(3) / 2  # Height of an equilateral triangle
            #
            #             # Define the triangle vertices (centered around the origin initially)
            #             triangle_points = np.array([
            #                 [0, 0, 0],
            #                 [-base_length / 2, height, 0.0],  # Left vertex
            #                 [base_length / 2, height, 0.0]  # Right vertex
            #                 # Top vertex
            #             ])
            #
            #             # Translate triangle to the center point
            #             triangle_points += center
            #
            #             # Define the connectivity of the triangle
            #             faces = np.array([[3, 0, 1, 2]])  # Single triangle face
            #             triangle = pv.PolyData(triangle_points, faces)
            #             self.plot.add_mesh(triangle, color='#000080', show_edges=True)

    def drawForces(self):
        for element in range(self.structure.elementlist.get_NumberOfElements()):
            self.ele_length = self.structure.elementlist.getElement(element).getLength()
        scale_factor = self.ele_length * self.symbolscale
        for node in range(self.structure.nodelist.get_NumberOfNodes()):
            position = self.structure.nodelist.getNode(node).getPosition()
            force_x = self.structure.nodelist.getNode(node).getForce().getComponents(0)
            force_y = self.structure.nodelist.getNode(node).getForce().getComponents(1)

            if force_x != 0:
                force = pv.Arrow(start=[position[0], position[1], 0],
                                 direction=[1, 0.0, 0.0], scale=scale_factor)
                self.plot.add_mesh(force, color="orange")

            if force_y != 0:
                force = pv.Arrow(start=[position[0], position[1], 0],
                                 direction=[0.0, 1, 0.0], scale=scale_factor)
                self.plot.add_mesh(force, color="orange")

    def drawDeformed(self, opacity: float):
        if opacity > 1:
            raise IndexError("Opacity greater than 1\nSet the value between 0 and 1")
        max_disp = max(self.structure.displacement)
        scale = 1.0
        # for node in range(self.structure.nodelist.get_NumberOfNodes()):
        #     grid = pv.StructuredGrid(*np.meshgrid(self.structure.nodelist.getNode(node).getPosition()[0],
        #                                           self.structure.nodelist.getNode(node).getPosition()[1], 0))
        #     scalar_field = grid.points[:, 0]  # Using the Z-coordinate in this example
        #     grid['scalars'] = scalar_field
        for element in range(self.structure.elementlist.get_NumberOfElements()):
            while max_disp * scale / self.ele_length < 0.5:
                scale += 0.5
            points = np.array([[self.structure.elementlist.getElement(element).getNode(0).getPosition()[0] +
                                scale * self.structure.elementlist.getElement(element).getNode(0).getDisplacement()[0],
                                self.structure.elementlist.getElement(element).getNode(0).getPosition()[1] +
                                scale * self.structure.elementlist.getElement(element).getNode(0).getDisplacement()[1],
                                0],
                               [self.structure.elementlist.getElement(element).getNode(1).getPosition()[0] +
                                scale * self.structure.elementlist.getElement(element).getNode(1).getDisplacement()[0],
                                self.structure.elementlist.getElement(element).getNode(1).getPosition()[1] +
                                scale * self.structure.elementlist.getElement(element).getNode(1).getDisplacement()[1],
                                0],
                               [self.structure.elementlist.getElement(element).getNode(2).getPosition()[0] +
                                scale * self.structure.elementlist.getElement(element).getNode(2).getDisplacement()[0],
                                self.structure.elementlist.getElement(element).getNode(2).getPosition()[1] +
                                scale * self.structure.elementlist.getElement(element).getNode(2).getDisplacement()[1],
                                0],
                               [self.structure.elementlist.getElement(element).getNode(3).getPosition()[0] +
                                scale * self.structure.elementlist.getElement(element).getNode(3).getDisplacement()[0],
                                self.structure.elementlist.getElement(element).getNode(3).getPosition()[1] +
                                scale * self.structure.elementlist.getElement(element).getNode(3).getDisplacement()[1],
                                0]
                               ])
            scalars = np.linspace(0, 1, points.shape[0])
            self.ele_length = self.structure.elementlist.getElement(element).getLength()
            faces = np.array([4, 0, 1, 2, 3])
            quad = pv.PolyData(points, faces)
            self.plot.add_mesh(quad, color='teal', show_edges=True, opacity=opacity)
            self.plot.set_background("white")

    def plotAll(self):
        self.plot.show()
