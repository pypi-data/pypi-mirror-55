from pycsp3 import *

nPieces, pieceLength, items = data.nPieces, data.pieceLength, data.items
nItems = len(items)
itemLengths = [item.length for item in items]

# p[i] is 1 iff the ith piece of the stock is used
p = VarArray(size=[nPieces], dom={0, 1})

# r[i][j] is the number of items of type j built using stock piece i
r = VarArray(size=[nPieces, nItems], dom=lambda i, j: range(items[j].demand+1))

satisfy(
    # each item demand must be exactly satisfied
    [Sum(r.col(i)) == item.demand for i, item in enumerate(items)],

    # each piece of the stock cannot provide more than its length
    [r[i] * itemLengths <= p[i] * pieceLength for i in range(nPieces)],

    # tag(symmetry-breaking)
    [Decreasing(p), LexDecreasing(r)]
)

minimize(
    Sum(p)
)
