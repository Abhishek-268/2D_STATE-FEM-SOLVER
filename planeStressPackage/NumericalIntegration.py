import numpy as np


class NumericalIntegration:
    def __init__(self, p: int):
        self.p = p
        self.gp = None
        self.xi1 = np.zeros(9)
        self.xi2 = np.zeros(9)
        self.alpha = np.zeros(3)

        if self.p == 1:
            self.gp = 1
            self.xi1[0] = 0
            self.xi2[0] = 0
            self.alpha[0] = 2

        elif self.p == 3:
            self.gp = 4
            self.xi1[0] = -1/np.sqrt(3)
            self.xi1[1] = 1/np.sqrt(3)
            self.xi1[2] = 1 / np.sqrt(3)
            self.xi1[3] = -1 / np.sqrt(3)
            self.xi2[0] = -1/np.sqrt(3)
            self.xi2[1] = -1 / np.sqrt(3)
            self.xi2[2] = 1 / np.sqrt(3)
            self.xi2[3] = 1 / np.sqrt(3)
            self.alpha[0] = 1
            self.alpha[1] = 1

        elif self.p == 5:
            self.gp = 9
            self.xi1[0] = -np.sqrt(3/5)
            self.xi1[1] = 0
            self.xi1[2] = np.sqrt(3/5)
            self.xi1[3] = np.sqrt(3 / 5)
            self.xi1[4] = np.sqrt(3 / 5)
            self.xi1[5] = 0
            self.xi1[6] = -np.sqrt(3 / 5)
            self.xi1[7] = -np.sqrt(3 / 5)
            self.xi1[8] = 0
            self.xi2[0] = -np.sqrt(3/5)
            self.xi2[1] = -np.sqrt(3/5)
            self.xi2[2] = -np.sqrt(3/5)
            self.xi2[3] = 0
            self.xi2[4] = np.sqrt(3/5)
            self.xi2[5] = np.sqrt(3 / 5)
            self.xi2[6] = np.sqrt(3 / 5)
            self.xi2[7] = 0
            self.xi2[8] = 0

            self.alpha[0] = 5/9
            self.alpha[1] = 8/9
            self.alpha[2] = 5/9

    def get_xi1(self):
        return self.xi1

    def get_xi2(self):
        return self.xi2

    def get_alpha(self):
        return self.alpha

    def get_p(self):
        return self.p

    def get_gp(self):
        return self.gp
