from pycsp3 import *

minIngredients, maxSize, pizza = data.minIngredients, data.maxSize, data.pizza
nRows, nCols = len(pizza), len(pizza[0])
patterns = [(i, j) for i in range(1, min(maxSize, nRows) + 1) for j in range(1, min(maxSize, nCols) + 1) if 2 * minIngredients <= i * j <= maxSize]
nPatterns = len(patterns)


def possible_slice(i, j, height, width):
    n_mushrooms, n_tomatoes = 0, 0
    for ib, jb in product(range(i, min(i + height, nRows)), range(j, min(j + width, nCols))):
        if pizza[ib][jb] == 0:
            n_mushrooms += 1
        else:
            n_tomatoes += 1
    return n_mushrooms >= minIngredients and n_tomatoes >= minIngredients


def possible_slices():
    _overlaps = [[[] for j in range(nCols)] for i in range(nRows)]
    _possibleSlices = [[[False for _ in range(nPatterns)] for _ in range(nCols)] for _ in range(nRows)]
    for i, j, k in product(range(nRows), range(nCols), range(nPatterns)):
        height, width = patterns[k][0], patterns[k][1]
        _possibleSlices[i][j][k] = possible_slice(i, j, height, width)
        if _possibleSlices[i][j][k]:
            for ib, jb in product(range(i, min(i + height, nRows)), range(j, min(j + width, nCols))):
                _overlaps[ib][jb].append((i, j, k))
    return _overlaps, _possibleSlices


overlaps, slices = possible_slices()


def pattern_size(i, j, k):
    return (min(i + patterns[k][0], nRows) - i) * (min(j + patterns[k][1], nCols) - j)


# x[i][j][k] is 1 iff the slice with left top cell at (i,j) and pattern k is selected
x = VarArray(size=[nRows, nCols, nPatterns], dom={0, 1}, when=lambda i, j, k: slices[i][j][k])

# s[i][j][k] is the size of the slice with left top cell at (i,j) and pattern k is selected (0 if the slice is not selected)
s = VarArray(size=[nRows, nCols, nPatterns], dom=lambda i, j, k: {0, pattern_size(i, j, k)}, when=lambda i, j, k: slices[i][j][k])

satisfy(
    [(x[i][j][k], s[i][j][k]) in [(0, 0), (1, pattern_size(i, j, k))] for i, j, k in product(range(nRows), range(nCols), range(nPatterns)) if slices[i][j][k]],

    [Sum([x[t[0]][t[1]][t[2]] for t in overlaps[i][j]]) <= 1 for i in range(nRows) for j in range(nCols) if len(overlaps[i][j]) > 1]
)

maximize(
    Sum(s)
)
