import numpy as np
import pandas as pd
from pygmsh.geo import Geometry as geom
from pygmsh.common.point import Point as Point
import sys

class Geometry:
    def __init__(self, csvFilename: str):
        self.filename = csvFilename
        self.df = pd.DataFrame(pd.read_csv(csvFilename)).astype(float)
        p1 = self.df.iloc[0, :]
        p2 = self.df.iloc[1, :]
        p3 = self.df.iloc[2, :]
        p4 = self.df.iloc[3, :]
        self.pointList = np.array([p1, p2, p3, p4])
        # x_coord = self.df.iloc[:, 0]
        # y_coord = self.df.iloc[:, 1]
        # self.dataList = np.empty((self.df.shape[0], 2),dtype=float)
        # for i in range(self.df.shape[0]):
        #     self.dataList[i, 0] = x_coord[i]
        #     self.dataList[i, 1] = y_coord[i]
        # self.pointList = [Point]
        # for i in range(self.df.shape[0]):
        #     self.pointList[i] = Point(0, (self.dataList[i]))
        # lineList = []
        # for i in range(len( self.pointList) - 1):
        #     lineList.append(geom.add_line( self.pointList[i],  self.pointList[i+1]))
        # tmp = []
        # for i in range(len(lineList) - 1):
        #     tmp = tmp.append(lineList[i])
        # loop = geom.add_curve_loop(tmp)
        # self.surface = None
        # self.surface = geom.add_plane_surface(loop)
        # geom.set_recombined_surfaces(surfaces=[self.surface])
        # self.mesh = geom.generate_mesh(self.surface)

    def getPoint(self, idx: int):
        return self.pointList[idx]

    def setPoint(self, idx: int, position: float):
        self.pointList[idx] = position
