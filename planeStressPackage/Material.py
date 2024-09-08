import numpy as np
from numpy.f2py.auxfuncs import throw_error


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

    def get_C(self, type: int):
        # IF type = 0 --> Plane_Stress
        # IF type = 1 --> Plane_Strain
        if type == 0:
            konst = self.getEModulus() / (1 - np.pow(self.getPoissonRatio(), 2))
            self.cMatrix = konst * np.array([[1, self.getPoissonRatio(), 0],
                                             [self.getPoissonRatio(), 1, 0],
                                             [0, 0, (1 - self.getPoissonRatio()) * 0.5],
                                             ])
            return self.cMatrix

        elif type == 1:
            konst = self.getEModulus() / ((1 + self.getPoissonRatio()) * (1 - 2* self.getPoissonRatio()))
            self.cMatrix = konst * np.array([[1 - self.getPoissonRatio(), self.getPoissonRatio(), 0],
                                             [self.getPoissonRatio(), 1 - self.getPoissonRatio(), 0],
                                             [0, 0, (1 - 2 * self.getPoissonRatio()) * 0.5],
                                             ])
            return self.cMatrix

        else:
            raise Exception("Choose one of the above values for the appropriate type: 0 --> plane stress" +
                            "1 --> plane strain")

