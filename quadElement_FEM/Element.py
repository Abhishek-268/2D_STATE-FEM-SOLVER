import numpy as np
from quadElement_FEM.NodeList import NodeList
from quadElement_FEM.NumericalIntegration import NumericalIntegration
from quadElement_FEM.Material import Material
from scipy.sparse import csr_matrix
from quadElement_FEM.Node import Node


class Element:
    def __init__(self, nodelist: NodeList, material: Material, case_type: int, ni: NumericalIntegration, height: float):
        self.B = np.zeros((3, 8))
        self.stress = np.zeros((3,1))
        self.nodelist = nodelist
        self.dN_dX = None
        self.length = np.zeros(2)
        self.jacobian = None
        self.material = material
        self.nodes = []
        self.dofNumbers = np.zeros(8)
        self.shapeFunctions = None
        self.N = None
        self.dN_dXi = np.zeros((2, 4))
        self.ni = ni
        self.h = height
        self.state_type = case_type
        self.strain = np.zeros((3,1))

    def getNode(self, idx: int):
        return self.nodes[idx]

    def setNode(self, idx:int, node: Node):
        self.nodes.insert(idx, node)

    def enumerateDOFs(self):
        for i in range(len(self.getNode(0).getDOFNumbers())):
            self.dofNumbers[i] = self.getNode(0).getDOFNumbers()[i]

        for i, j in zip(range(2, 4), range(len(self.getNode(1).getDOFNumbers()))):
            self.dofNumbers[i] = self.getNode(1).getDOFNumbers()[j]

        for i, j in zip(range(4, 6), range(len(self.getNode(2).getDOFNumbers()))):
            self.dofNumbers[i] = self.getNode(2).getDOFNumbers()[j]

        for i, j in zip(range(6, 8), range(len(self.getNode(3).getDOFNumbers()))):
            self.dofNumbers[i] = self.getNode(3).getDOFNumbers()[j]

    def getDOFNumbers(self):
        return self.dofNumbers

    def computeStiffnessMatrix(self):
        k = np.zeros((8, 8))
        for i in range(self.ni.get_gp()):
            self.N = np.array([0.25 * (1 - self.ni.get_xi1()[i]) * (1 - self.ni.get_xi2()[i]),
                               0.25 * (1 + self.ni.get_xi1()[i]) * (1 - self.ni.get_xi2()[i]),
                               0.25 * (1 + self.ni.get_xi1()[i]) * (1 + self.ni.get_xi2()[i]),
                               0.25 * (1 - self.ni.get_xi1()[i]) * (1 + self.ni.get_xi2()[i])])

            self.dN_dXi = np.array([[-0.25 * (1 - self.ni.get_xi2()[i]),
                                      0.25 * (1 - self.ni.get_xi2()[i]),
                                      0.25 * (1 + self.ni.get_xi2()[i]),
                                     -0.25 * (1 + self.ni.get_xi2()[i])],
                                    [-0.25 * (1 - self.ni.get_xi1()[i]),
                                     -0.25 * (1 + self.ni.get_xi1()[i]),
                                      0.25 * (1 + self.ni.get_xi1()[i]),
                                      0.25 * (1 - self.ni.get_xi1()[i])]
                                    ])
            dX = np.zeros((4, 2))
            for u in range(2):
                dX[0, u] = self.getNode(0).getPosition()[u]
            for u in range(2):
                dX[1, u] = self.getNode(1).getPosition()[u]
            for u in range(2):
                dX[2, u] = self.getNode(2).getPosition()[u]
            for u in range(2):
                dX[3, u] = self.getNode(3).getPosition()[u]
            self.jacobian = np.dot(self.dN_dXi, dX)

            j_inv = np.linalg.inv(self.jacobian)
            j_det = np.linalg.det(self.jacobian)
            self.dN_dX = j_inv @ self.dN_dXi
            self.B[0, 0] = self.dN_dX[0, 0]
            self.B[1, 0] = 0
            self.B[2, 0] = self.dN_dX[1, 0]
            self.B[0, 1] = 0
            self.B[1, 1] = self.dN_dX[1, 0]
            self.B[2, 1] = self.dN_dX[0, 0]
            self.B[0, 2] = self.dN_dX[0, 1]
            self.B[1, 2] = 0
            self.B[2, 2] = self.dN_dX[1, 1]
            self.B[0, 3] = 0
            self.B[1, 3] = self.dN_dX[1, 1]
            self.B[2, 3] = self.dN_dX[0, 1]
            self.B[0, 4] = self.dN_dX[0, 2]
            self.B[1, 4] = 0
            self.B[2, 4] = self.dN_dX[1, 2]
            self.B[0, 5] = 0
            self.B[1, 5] = self.dN_dX[1, 2]
            self.B[2, 5] = self.dN_dX[0, 2]
            self.B[0, 6] = self.dN_dX[0, 3]
            self.B[1, 6] = 0
            self.B[2, 6] = self.dN_dX[1, 3]
            self.B[0, 7] = 0
            self.B[1, 7] = self.dN_dX[1, 3]
            self.B[2, 7] = self.dN_dX[0, 3]
            a1 = self.ni.get_alpha()[0]
            a2 = self.ni.get_alpha()[1]
            c = self.material.get_C(self.state_type)
            b_transpose = np.transpose(self.B)
            k_gp = (a1 * a2 * self.h * j_det *
                    np.dot(np.dot(b_transpose, c), self.B))

            for l in range(k.shape[0]):
                for j in range(k.shape[0]):
                    k[l, j] += k_gp[l, j]

        k_csr = csr_matrix(k)
        return k

    def getLength(self):
        for i in range(len(self.length)):
            self.length[i] = np.abs(self.getNode(1).position[i]-self.getNode(0).position[i])
        return np.sqrt(np.pow(self.length[0], 2)+np.pow(self.length[1], 2))

    def get_strain(self):
        strain = np.zeros((3, 1))
        u = np.zeros((8, 1))
        B = self.B
        for j in range(self.nodelist.get_NumberOfNodes()):
                u[2 * j, 0] += self.nodelist.getNode(j).getDisplacement()[0]
                u[2 * j + 1, 0] += self.nodelist.getNode(j).getDisplacement()[1]
                strain = np.matmul(B, u)
        self.strain = strain
        return self.strain
    
    def get_stress(self):
        self.stress = np.matmul(self.material.get_C(self.state_type), self.get_strain())
        return self.stress
