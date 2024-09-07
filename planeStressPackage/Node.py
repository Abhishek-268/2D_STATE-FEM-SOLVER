import numpy as np
from planeStressPackage.Constraint import Constraint
from planeStressPackage.Force import Force


class Node:

    def __init__(self, x1: float, x2: float):
        self.constraint = Constraint(True, True)
        self.force = Force(0, 0)
        self.dofNumbers = np.zeros(2)
        self.position = [x1, x2]
        self.displacement = np.zeros(2)

    def setConstraint(self, c: Constraint):
        self.constraint = c

    def getConstraint(self):
        return self.constraint

    def setForce(self, force: Force):
        self.force = force

    def getForce(self):
        return self.force

    def enumerateDOFs(self, start: int):
        for i in range(len(self.dofNumbers)):
            if self.getConstraint().isFree(i) is True:
                self.dofNumbers[i] = start
                start += 1
            else:
                self.dofNumbers[i] = -1
        return start

    def getDOFNumbers(self):
        return self.dofNumbers

    def getPosition(self):
        return self.position

    def setDisplacement(self, i: int, value: np.float64):
        self.displacement[i] = value

    def getDisplacement(self):
        return self.displacement

    def print(self):
        print("The position of Node is : ")
        direction = ["X", "Y"]
        for i in range(len(direction)):
            print("In " + str(direction[i]) + " " + str(self.getPosition()[i]))
