import numpy as np
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix
from planeStressPackage.NodeList import NodeList
from planeStressPackage.ElementList import ElementList


class Structure:
    def __init__(self, nodelist: NodeList, elementlist: ElementList):
        self.nodelist = nodelist
        self.elementlist = elementlist
        self.DOFs = []
        self.displacement = []

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
        row_to_remove = []
        rglobal = np.zeros((8, 1))
        rglobal[0] = self.nodelist.getNode(0).getForce().getComponents(0)
        rglobal[1] = self.nodelist.getNode(0).getForce().getComponents(1)
        rglobal[2] = self.nodelist.getNode(1).getForce().getComponents(0)
        rglobal[3] = self.nodelist.getNode(1).getForce().getComponents(1)
        rglobal[4] = self.nodelist.getNode(2).getForce().getComponents(0)
        rglobal[5] = self.nodelist.getNode(2).getForce().getComponents(1)
        rglobal[6] = self.nodelist.getNode(3).getForce().getComponents(0)
        rglobal[7] = self.nodelist.getNode(3).getForce().getComponents(1)
        for i in range(self.elementlist.get_NumberOfElements()):
            if not self.elementlist.getElement(i).getNode(0).getConstraint().isFree(0):
                row_to_remove.append(0)

            if not self.elementlist.getElement(i).getNode(0).getConstraint().isFree(1):
                row_to_remove.append(1)

            if not self.elementlist.getElement(i).getNode(1).getConstraint().isFree(0):
                row_to_remove.append(2)

            if not self.elementlist.getElement(i).getNode(1).getConstraint().isFree(1):
                row_to_remove.append(3)

            if not self.elementlist.getElement(i).getNode(2).getConstraint().isFree(0):
                row_to_remove.append(4)

            if not self.elementlist.getElement(i).getNode(2).getConstraint().isFree(1):
                row_to_remove.append(5)

            if not self.elementlist.getElement(i).getNode(3).getConstraint().isFree(0):
                row_to_remove.append(6)

            if not self.elementlist.getElement(i).getNode(3).getConstraint().isFree(1):
                row_to_remove.append(7)

        rglobal_red = np.delete(rglobal, row_to_remove, axis=0)
        rglobal_csr = csr_matrix(rglobal_red)
        return rglobal_csr


    def assembleStiffnessMatrix(self):
        KGlobal = np.zeros((self.nodelist.get_NumberOfNodes() * 2, self.nodelist.get_NumberOfNodes() * 2))

        row_to_remove = []
        col_to_remove = []
        KGlobal_red = []

        for i in range(self.elementlist.get_NumberOfElements()):
            KGlobal += self.elementlist.getElement(i).computeStiffnessMatrix()
            if not self.elementlist.getElement(i).getNode(0).getConstraint().isFree(0):
                row_to_remove.append(0)
                col_to_remove.append(0)
            if not self.elementlist.getElement(i).getNode(0).getConstraint().isFree(1):
                row_to_remove.append(1)
                col_to_remove.append(1)
            if not self.elementlist.getElement(i).getNode(1).getConstraint().isFree(0):
                row_to_remove.append(2)
                col_to_remove.append(2)
            if not self.elementlist.getElement(i).getNode(1).getConstraint().isFree(1):
                row_to_remove.append(3)
                col_to_remove.append(3)
            if not self.elementlist.getElement(i).getNode(2).getConstraint().isFree(0):
                row_to_remove.append(4)
                col_to_remove.append(4)
            if not self.elementlist.getElement(i).getNode(2).getConstraint().isFree(1):
                row_to_remove.append(5)
                col_to_remove.append(5)
            if not self.elementlist.getElement(i).getNode(3).getConstraint().isFree(0):
                row_to_remove.append(6)
                col_to_remove.append(6)
            if not self.elementlist.getElement(i).getNode(3).getConstraint().isFree(1):
                row_to_remove.append(7)
                col_to_remove.append(7)
            KGlobal_red_row = np.delete(KGlobal, row_to_remove, axis=0)
            KGlobal_red = np.delete(KGlobal_red_row, col_to_remove, axis=1)
        KGlobal_csr = csr_matrix(KGlobal_red)

        return KGlobal_csr

    def solve(self):
        self.enumerateDOFs()
        kGlobal = self.assembleStiffnessMatrix()
        rGlobal = self.assembleLoadVector()
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
        nodes = [1, 2, 3, 4]
        for node in range(self.nodelist.get_NumberOfNodes()):
            print("\nNode" + str(nodes[node]), self.nodelist.getNode(node).getDisplacement())
