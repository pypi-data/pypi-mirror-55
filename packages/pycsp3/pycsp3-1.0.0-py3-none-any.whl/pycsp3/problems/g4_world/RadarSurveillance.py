#  This is a Radar surveillance instance where " + nRadars + " radars must be put on a geographic area of size " + mapSize + "*" + mapSize + "." There
#  are " + nInsignificantCells + " insignificant cells that must not be covered by any radar. All other cells must be covered by exactly " +
#  maxCoverage + " radars." + " This instance has been generated using a seed equal to " + seed . This instance follows the description given by the
#  Swedish Institute of Computer Science (SICS).

from pycsp3 import *
from enum import Enum


class Sector(Enum):
    NEAST = 0  # north east
    EAST = 1
    SEAST = 2  # south east
    SWEST = 3  # south west
    WEST = 4
    NWEST = 5  # north west

    def row_right_cell(self, i):
        return i + (-1 if self in {Sector.NEAST, Sector.NWEST} else 0 if self in {Sector.EAST, Sector.WEST} else 1)

    def row_left_cell(self, i):
        return i + (-1 if self in {Sector.NEAST, Sector.EAST} else 0 if self in {Sector.SEAST, Sector.NWEST} else 1)

    def col_right_cell(self, i, j):
        ro = i % 2 == 1
        return j + (
            1 if self == Sector.EAST else -1 if self == Sector.WEST else (0 if ro else 1) if self in {Sector.NEAST, Sector.SEAST} else (-1 if ro else 0))

    def col_left_cell(self, i, j):
        ro = i % 2 == 1
        return j + (
            1 if self == Sector.SEAST else -1 if self == Sector.NWEST else (0 if ro else 1) if self in {Sector.EAST, Sector.SWEST} else (-1 if ro else 0))


def distance(iCell, jCell, iCurr, jCurr, sector, currDistance, maxDistance):
    if currDistance > maxDistance:
        return -1
    if iCell == iCurr and jCell == jCurr:
        return currDistance
    d = distance(iCell, jCell, sector.row_right_cell(iCurr), sector.col_right_cell(iCurr, jCurr), sector, currDistance + 1, maxDistance)
    if d != -1:
        return d
    return distance(iCell, jCell, sector.row_left_cell(iCurr), sector.col_left_cell(iCurr, jCurr), sector, currDistance + 1, maxDistance)


def isInsignificant(iCell, jCell):
    return any(t[0] == iCell and t[1] == jCell for t in insignificantCells)


def dealWithCell(iCell, jCell, maximumDistance):
    vars = []
    dists = []
    for i in range(len(radars)):
        for sector in list(Sector):
            d = distance(iCell, jCell, sector.row_right_cell(radars[i][0]), sector.col_right_cell(radars[i][0], radars[i][1]), sector, 1, maximumDistance)
            if d != -1:
                vars.append(x[i][sector.value])
                dists.append(d)
    if len(vars) == 0:
        return None
    if len(vars) == 1:
        return vars[0] < dists[0] if isInsignificant(iCell, jCell) else vars[0] > dists[0] - 1
    args = [vars[i] >= dists[i] for i in range(len(vars))]
    return Sum(args) == (0 if isInsignificant(iCell, jCell) else min(len(vars), maxCoverage))


mapSize, maxCoverage = data.mapSize, data.maxCoverage
radars = data.radars
insignificantCells = data.insignificantCells
nRadars, nSectors = len(radars), len(Sector)

x = VarArray(size=[nRadars, nSectors], dom=range(maxCoverage + 1))

satisfy(
    dealWithCell(i, j, maxCoverage) for i in range(mapSize) for j in range(mapSize)  # if dealWithCell(i, j, maxCoverage)
)
