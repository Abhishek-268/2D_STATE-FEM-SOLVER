import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

from quadElement_FEM.Element import Element
from quadElement_FEM.Node import Node



class Structure:
    def __init__(self):
        self.nodeList = []
        self.elementList = []
        self.DOFs = []

    def addNode(self, x1: float, x2: float, x3: float):
        node1 = Node(x1, x2, x3)
        self.nodeList.append(node1)
        return node1

    def addElement(self, e: float, a: float, n1: int, n2: int):
        element1 = Element(eModulus=e, area=a, n1=self.nodeList[n1], n2=self.nodeList[n2])
        self.elementList.append(element1)
        return element1

    def getNumberOfNodes(self):
        return len(self.nodeList)

    def getNode(self, idx: int):
        return self.nodeList[idx]

    def getNumberOfElements(self):
        return len(self.elementList)

    def getElement(self, idx: int):
        return self.elementList[idx]

    def enumerateDOFs(self):
        start = 0
        for i in range(self.getNumberOfNodes()):
            start = self.getNode(i).enumerateDOFs(start)

        for j in range(self.getNumberOfElements()):
            self.getElement(j).enumerateDOFs()

    def printStructure(self):
        print("SUMMARY STRUCTURE")
        for node in range(self.getNumberOfNodes()):
            print("\nNode" + str(node), self.getNode(node).getPosition())
            for constraint in range(3):
                print("\nConstraints" + str(constraint), self.getNode(node).getConstraint().print())
            for force in range(3):
                print("\nForce" + str(force), self.getNode(node).getForce().print())
        for element in range(self.getNumberOfElements()):
            print("\nElement" + str(element), self.getElement(element).print())

    def assembleLoadVector(self):
        rlocal = []
        rglobal = []
        totalDOFs: int = 0
        for node in range(self.getNumberOfNodes()):
            # The `enumerateDOFs` method updates `start`, so we should calculate total DOFs separately
            dofs = self.getNode(node).getDOFNumbers()
            totalDOFs += sum(dof != -1 for dof in dofs)

        rGlobal = np.zeros(totalDOFs)

        currentIndex = 0
        for node in range(self.getNumberOfNodes()):
            dof = self.getNode(node).getDOFNumbers()
            forceComponents = self.getNode(node).getForce().components

            for i in range(len(dof)):
                if dof[i] != -1:
                    rGlobal[int(dof[i])] = forceComponents[i]
        rglobal_csr = csr_matrix(rglobal)
        return rGlobal

    def assembleStiffnessMatrix(self):

        # Determine total number of DOFs
        totalDOFs = 0
        for node in range(self.getNumberOfNodes()):
            dofs = self.getNode(node).getDOFNumbers()
            totalDOFs += sum(dof != -1 for dof in dofs)

        KGlobal = np.zeros((totalDOFs, totalDOFs))

        for element in range(self.getNumberOfElements()):
            # Get the local stiffness matrix of the element
            kLocal = self.getElement(element).computeStiffnessMatrix().toarray()

            # Get the DOFs for this element
            dofNumbers = self.getElement(element).getDOFNumbers()

            # Assemble the local stiffness matrix into the global stiffness matrix
            for i in range(6):
                for j in range(6):
                    if dofNumbers[i] != -1 and dofNumbers[j] != -1:
                        KGlobal[int(dofNumbers[i]), int(dofNumbers[j])] += kLocal[i, j]
        KGlobal_csr = csr_matrix(KGlobal)
        return KGlobal_csr

    def solve(self):
        self.enumerateDOFs()
        kGlobal = self.assembleStiffnessMatrix()
        rGlobal = self.assembleLoadVector()
        displacement = spsolve(kGlobal, rGlobal)
        for node in range(self.getNumberOfNodes()):
            dofs = self.getNode(node).getDOFNumbers()
            for i, dof in enumerate(dofs):
                if dof != -1:
                    self.getNode(node).setDisplacement(i, displacement[int(dof)])
        return displacement

    def printResults(self):
        print("\nANALYSIS RESULTS\nDisplacements")
        for node in range(self.getNumberOfNodes()):
            print("\nNode" + str(node), self.getNode(node).getDisplacement())

        for element in range(self.getNumberOfElements()):
            print("\nElement" + str(element), self.getElement(element).computeForce())