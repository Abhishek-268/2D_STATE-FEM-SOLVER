class Constraint:
    def __init__(self, u1: bool, u2: bool):
        self.free = [u1, u2]

    def isFree(self, c: int):
        return self.free[c]

    def print(self):
        direction = ["X", "Y"]
        print("The constraints are ")
        for i in range(len(self.free)):
            print("\nIn " + str(direction[i]) + "  " + str(self.free[i]))
            