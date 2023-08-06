from pycsp3 import *

# Problem 054 at CSPLib

n = data.n

# q[i] is the column where is put the ith queen (at row i)
q = VarArray(size=n, dom=range(n))

if not variant():
    satisfy(
        AllDifferent(q),

        # controlling no two queens on the same upward diagonal
        AllDifferent(q[i] + i for i in range(n)),

        # controlling no two queens on the same downward diagonal
        AllDifferent(q[i] - i for i in range(n))
    )
elif variant("v1"):
    satisfy(
        AllDifferent(q),

        [dist(q[i], q[j]) != dist(i, j) for i in range(n) for j in range(i + 1, n)]
    )

if variant("v2"):
    satisfy(
        (q[i] != q[j]) & (dist(q[i], q[j]) != dist(i, j)) for i in range(n) for j in range(i + 1, n)
    )
