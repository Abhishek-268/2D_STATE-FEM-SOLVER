import numpy as np
import pandas as pd
from pygmsh.geo import Geometry as geom
from pygmsh.common.point import Point as Point
import sys

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
