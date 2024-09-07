import numpy as np
from PyPlus.Node import Node
from scipy.sparse import csr_matrix


class TrussElement:
    def __init__(self, eModulus: float, area: float, n1: Node, n2: Node):
        self.area = area
        self.eModulus = eModulus
        self.n1 = n1
        self.n2 = n2
        self.dofNumbers = np.zeros(6)
        self.force = np.zeros(3)
        self.length = np.zeros(3)

    def computeStiffnessMatrix(self):
        l = (self.getNode2().getPosition()[0] - self.getNode1().getPosition()[0])/self.getLength()
        m = (self.getNode2().getPosition()[1] - self.getNode1().getPosition()[1])/self.getLength()
        n = (self.getNode2().getPosition()[2] - self.getNode1().getPosition()[2])/self.getLength()
        matrix = np.array([
            [l*l,  l*m,  l*n, -l*l, -l*m, -l*n],
            [l*m,  m*m,  m*n, -l*m, -m*m, -m*n],
            [l*n,  m*n,  n*n, -l*n, -m*n, -n*n],
            [-l*l, -l*m, -l*n,  l*l,  l*m,  l*n],
            [-l*m, -m*m, -m*n,  l*m,  m*m,  m*n],
            [-l*n, -m*n, -n*n,  l*n,  m*n,  n*n]
                           ])
        scalars = (self.getEModulus() * self.getArea() / self.getLength())
        stiffnessMatrix = matrix * scalars
        csr = csr_matrix(stiffnessMatrix)
        return csr

    def enumerateDOFs(self):
        for i in range(len(self.getNode1().getDOFNumbers())):
            self.dofNumbers[i] = self.getNode1().getDOFNumbers()[i]

        for i, j in zip(range(3, 6), range(len(self.getNode2().getDOFNumbers()))):
            self.dofNumbers[i] = self.getNode2().getDOFNumbers()[j]

    def getDOFNumbers(self):
        return self.dofNumbers

    def computeForce(self):
        return self.getE1() * self.getEModulus() * self.getArea()

    def getE1(self):
        e1 = (self.getNode2().getDisplacement() - self.getNode1().getDisplacement())/self.getLength()
        return e1

    def getLength(self):
        for i in range(len(self.length)):
            self.length[i] = np.abs(self.n2.position[i]-self.n1.position[i])
        return np.sqrt(np.pow(self.length[0], 2)+np.pow(self.length[1], 2)+np.pow(self.length[2], 2))

    def getNode1(self):
        return self.n1

    def getNode2(self):
        return self.n2

    def getArea(self):
        return self.area

    def getEModulus(self):
        return self.eModulus

    def print(self):
        print("Truss_Element contains 2 Nodes" + "\nStiffness Matrix : " + "\n" +
              str(self.computeStiffnessMatrix().toarray()) +
              "\nArea is : " + str(self.area) + "\nLength : " + str(self.getLength()))
