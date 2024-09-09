class Force:
    def __init__(self, r1: float = 0, r2: float = 0):
        self.r1 = r1
        self.r2 = r2
        self.components = [r1, r2]

    def getComponents(self, c: int):
        while 0 <= c < len(self.components):
            return self.components[c]
        else:
            return IndexError("Component index invalid")

    def print(self):
        direction = ["X", "Y"]
        print("The components of Force are:")
        for i in range(len(self.components)):
            print("\nIn " + str(direction[i]) + str(self.components[i]))
