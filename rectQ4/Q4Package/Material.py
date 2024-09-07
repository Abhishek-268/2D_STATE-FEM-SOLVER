import numpy as np


class Material:
    def __init__(self, eModulus: float, poissonRatio: float):
        self.eModulus = eModulus
        self.poissonRatio = poissonRatio
        self.cMatrix = np.zeros((3, 3))

    def getEModulus(self):
        return self.eModulus

    def setEModulus(self, value: float):
        self.eModulus = value

    def getPoissonRatio(self):
        return self.poissonRatio

    def setPoissonRatio(self, val: float):
        self.poissonRatio = val

    def planeStress_C(self):
        konst = self.getEModulus()/(1 - np.pow(self.getPoissonRatio(), 2))
        tmp = np.array([[1, self.getPoissonRatio(), 0],
                        [self.getPoissonRatio(), 1, 0],
                        [0, 0, (1-self.getPoissonRatio()) * 0.5],
                        ])
        self.cMatrix = np.dot(konst, tmp)

    def get_planeStress_C(self):
        return self.cMatrix
