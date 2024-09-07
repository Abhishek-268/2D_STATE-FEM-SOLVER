class Force:
    def __init__(self, r1: float, r2: float):
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
