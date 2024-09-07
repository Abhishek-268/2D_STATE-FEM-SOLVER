import numpy as np
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix
from Q4Package.NodeList import NodeList
from Q4Package.ElementList import ElementList


class Structure:
    def __init__(self, nodelist: NodeList, elementlist: ElementList):
        self.nodelist = nodelist
        self.elementlist = elementlist
        self.DOFs = []

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

    def assembleLoadVector(self):
        rglobal = np.zeros((8, 1))
        rglobal[0] = self.nodelist.getNode(0).getForce().getComponents(0)
        rglobal[1] = self.nodelist.getNode(0).getForce().getComponents(1)
        rglobal[2] = self.nodelist.getNode(1).getForce().getComponents(0)
        rglobal[3] = self.nodelist.getNode(1).getForce().getComponents(1)
        rglobal[4] = self.nodelist.getNode(2).getForce().getComponents(0)
        rglobal[5] = self.nodelist.getNode(2).getForce().getComponents(1)
        rglobal[6] = self.nodelist.getNode(3).getForce().getComponents(0)
        rglobal[7] = self.nodelist.getNode(3).getForce().getComponents(1)
        rglobal_csr = csr_matrix(rglobal)
        return rglobal_csr

    def assembleStiffnessMatrix(self):
        KGlobal = np.zeros((8, 8))
        for i in range(self.elementlist.get_NumberOfElements()):
            KGlobal += self.elementlist.getElement(i).computeStiffnessMatrix(1)
        KGlobal_csr = csr_matrix(KGlobal)
        return KGlobal_csr

    def solve(self):
        # self.enumerateDOFs()
        kGlobal = self.assembleStiffnessMatrix()
        rGlobal = self.assembleLoadVector()
        displacement = spsolve(kGlobal, rGlobal)
        for node in range(self.nodelist.get_NumberOfNodes()):
            dofs = self.nodelist.getNode(node).getDOFNumbers()
            for i, dof in enumerate(dofs):
                if dof != -1:
                    self.nodelist.getNode(node).setDisplacement(i, displacement[int(dof)])
        return displacement

    def printResults(self):
        print("\nANALYSIS RESULTS\nDisplacements")
        for node in range(self.nodelist.get_NumberOfNodes()):
            print("\nNode" + str(node), self.nodelist.getNode(node).getDisplacement())

        for element in range(self.elementlist.get_NumberOfElements()):
            print("\nElement" + str(element), self.elementlist.getElement(element).computeForce())
