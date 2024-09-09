import pandas as pd

class Geometry:
    def __init__(self, csvFilename: str):
        self.filename = csvFilename
        self.df = pd.DataFrame(pd.read_csv(csvFilename)).astype(float)
        self.pointList = []
        for i in range(self.df.shape[0]):
            self.pointList.append(self.df.iloc[i, :])

    def getPoint(self, idx: int):
        return self.pointList[idx]

    def setPoint(self, idx: int, position: float):
        self.pointList[idx] = position
