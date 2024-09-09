import numpy as np
import pandas as pd
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix
from quadElement_FEM.NodeList import NodeList
from quadElement_FEM.ElementList import ElementList


class Structure:
    def __init__(self, nodelist: NodeList, elementlist: ElementList):
        self.nodelist = nodelist
        self.elementlist = elementlist
        self.DOFs = []
        self.displacement = []
        self.connectivity_matrix = None

    def enumerateDOFs(self):
        start = 0
        for i in range(self.nodelist.get_NumberOfNodes()):
            start = self.nodelist.getNode(i).enumerateDOFs(start)

        for j in range(self.elementlist.get_NumberOfElements()):
            self.elementlist.getElement(j).enumerateDOFs()

    def printStructure(self):
        print("SUMMARY STRUCTURE")
        for node in range(self.nodelist.get_NumberOfNodes()):
            print("\nNode" + str(node), self.nodelist.getNode(node).getPosition())
            for constraint in range(3):
                print("\nConstraints" + str(constraint), self.nodelist.getNode(node).getConstraint().print())
            for force in range(3):
                print("\nForce" + str(force), self.nodelist.getNode(node).getForce().print())
        for element in range(self.elementlist.get_NumberOfElements()):
            print("\nElement" + str(element), self.elementlist.getElement(element).print())

    def assembleLoadVector(self, mesh_data: str):
        connect_matrix = self.mesh(mesh_data)
        del_row = []
        dof_per_node = 2
        rglobal = np.zeros((self.nodelist.get_NumberOfNodes() * dof_per_node, 1))
        for element in connect_matrix:
            for i in range(self.nodelist.get_NumberOfNodes()):
                node = self.nodelist.getNode(i)
                rglobal[2 * i] += node.getForce().getComponents(0)
                rglobal[2 * i + 1] += node.getForce().getComponents(1)
        for i in range(self.nodelist.get_NumberOfNodes()):
            if not self.nodelist.getNode(i).getConstraint().isFree(0):
                del_row.append(2 * i)
            if not self.nodelist.getNode(i).getConstraint().isFree(1):
                del_row.append(2 * i + 1)
        # for row in del_row:
        #     rglobal[row] = 0
        rglobal = np.delete(rglobal, del_row, axis=0)
        rglobal_csr = csr_matrix(rglobal)
        return rglobal_csr

    def mesh(self, mesh_data: str):
        mesh = pd.read_csv(mesh_data)
        self.connectivity_matrix = mesh.iloc[:, 1:].to_numpy()
        return self.connectivity_matrix

    def assembly_function(self, global_K, local_K, element_nodes):
        # For each pair of nodes in the element
        for i in range(4):
            for j in range(4):
                # Global DOF indices for u_x and u_y for node i and node j
                global_i_x = 2 * element_nodes[i]
                global_i_y = 2 * element_nodes[i] + 1
                global_j_x = 2 * element_nodes[j]
                global_j_y = 2 * element_nodes[j] + 1

                # Add the local stiffness contributions to the global matrix
                global_K[global_i_x, global_j_x] += local_K[2 * i, 2 * j]
                global_K[global_i_x, global_j_y] += local_K[2 * i, 2 * j + 1]
                global_K[global_i_y, global_j_x] += local_K[2 * i + 1, 2 * j]
                global_K[global_i_y, global_j_y] += local_K[2 * i + 1, 2 * j + 1]


    def assembleStiffnessMatrix(self, mesh_data: str):
        self.mesh(mesh_data)
        KGlobal = np.zeros((self.nodelist.get_NumberOfNodes() * 2, self.nodelist.get_NumberOfNodes() * 2))
        row_to_remove = []
        col_to_remove = []
        Klocal_list = []

        for i in range(self.elementlist.get_NumberOfElements()):
            Klocal = self.elementlist.getElement(i).computeStiffnessMatrix()
            Klocal_list.append(Klocal)

        for e, element_nodes in enumerate(self.connectivity_matrix):
            local_K = Klocal_list[e]
            self.assembly_function(KGlobal, local_K, element_nodes)

        for j in range(self.nodelist.get_NumberOfNodes()):
            if not self.nodelist.getNode(j).getConstraint().isFree(0):
                row_to_remove.append(2 * j)
                col_to_remove.append(2 * j)
            if not self.nodelist.getNode(j).getConstraint().isFree(1):
                row_to_remove.append(2 * j + 1)
                col_to_remove.append(2 * j + 1)
        # for row in row_to_remove:
        #     KGlobal[row, :] = 0
        #     KGlobal[:, row] = 0
        #     KGlobal[row, row] = 1  # Set diagonal to 1 for stability
        #
        # for col in col_to_remove:
        #     KGlobal[col, :] = 0
        #     KGlobal[:, col] = 0
        #     KGlobal[col, col] = 1  # Set diagonal to 1 for stability
        KGlobal_red_row = np.delete(KGlobal, row_to_remove, axis=0)
        KGlobal_red = np.delete(KGlobal_red_row, col_to_remove, axis=1)
        KGlobal_csr = csr_matrix(KGlobal_red)
        return KGlobal_csr

    def solve(self, mesh_data: str):
        self.enumerateDOFs()
        kGlobal = self.assembleStiffnessMatrix(mesh_data)
        rGlobal = self.assembleLoadVector(mesh_data)
        displacement = spsolve(kGlobal, rGlobal)
        for node in range(self.nodelist.get_NumberOfNodes()):
            dofs = self.nodelist.getNode(node).getDOFNumbers()
            for i, dof in enumerate(dofs):
                if dof != -1:
                    self.nodelist.getNode(node).setDisplacement(i, displacement[int(dof)])
        self.displacement = displacement
        return displacement

    def printResults(self):
        print("\nANALYSIS RESULTS\nDisplacements")
        nodes = []
        for node in range(self.nodelist.get_NumberOfNodes()):
            nodes.append(node+1)
        for node in range(self.nodelist.get_NumberOfNodes()):
            print("\nNode " + str(nodes[node]), self.nodelist.getNode(node).getDisplacement())
        print("\nStrains")
        elements = []
        for element in range(self.elementlist.get_NumberOfElements()):
            elements.append(element+1)
        for element in range(self.elementlist.get_NumberOfElements()):
            print("\nElement " , str(elements[element]))
            print(self.elementlist.getElement(element).get_strain())
        print("\nStress")
        for element in range(self.elementlist.get_NumberOfElements()):
            print("\nElement " , str(elements[element]))
            print(self.elementlist.getElement(element).get_stress())

