import numpy as np
from Q4Package.NodeList import NodeList
from Q4Package.NumericalIntegration import NumericalIntegration
from Q4Package.Material import Material
# from scipy.sparse import csr_matrix


class Element:
    def __init__(self, nodelist: NodeList, material: Material, ni: NumericalIntegration):
        self.jacobian = None
        self.material = material
        self.nodelist = nodelist
        self.n1 = self.nodelist.getNode(0)
        self.n2 = self.nodelist.getNode(1)
        self.n3 = self.nodelist.getNode(2)
        self.n4 = self.nodelist.getNode(3)
        self.dofNumbers = np.zeros(8)
        self.shapeFunctions = None
        self.N = None
        self.dN_dXi = np.zeros((2,4))
        self.ni = ni

    def getNode1(self):
        return self.n1

    def getNode2(self):
        return self.n2

    def getNode3(self):
        return self.n3

    def getNode4(self):
        return self.n4

    def enumerateDOFs(self):
        for i in range(len(self.getNode1().getDOFNumbers())):
            self.dofNumbers[i] = self.getNode1().getDOFNumbers()[i]

        for i, j in zip(range(2, 4), range(len(self.getNode2().getDOFNumbers()))):
            self.dofNumbers[i] = self.getNode2().getDOFNumbers()[j]

        for i, j in zip(range(4, 6), range(len(self.getNode2().getDOFNumbers()))):
            self.dofNumbers[i] = self.getNode3().getDOFNumbers()[j]

        for i, j in zip(range(6, 8), range(len(self.getNode2().getDOFNumbers()))):
            self.dofNumbers[i] = self.getNode4().getDOFNumbers()[j]

    def getDOFNumbers(self):
        return self.dofNumbers

    def computeStiffnessMatrix(self, h: int):
        konst = ((self.material.getEModulus() * h) /
                 (12 * self.nodelist.get_a() * self.nodelist.get_b() *
                  (1 - np.pow(self.material.getPoissonRatio(), 2))
                  ))
        k = np.zeros((8, 8))
        k[0, 0] = konst * (4 * self.nodelist.get_a() * self.nodelist.get_a() +
                           2 * self.nodelist.get_b() * self.nodelist.get_b() * (1 - self.material.getPoissonRatio()))
        k[]
        # k_csr = csr_matrix(k)
        return k
