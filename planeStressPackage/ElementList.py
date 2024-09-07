import Element as Element


class ElementList:
    def __init__(self):
        self.ElementList = []

    def getElement(self, idx: int):
        return self.ElementList[idx]

    def setElement(self, element: Element):
        self.ElementList.append(element)

    def get_NumberOfElements(self):
        return len(self.ElementList)
