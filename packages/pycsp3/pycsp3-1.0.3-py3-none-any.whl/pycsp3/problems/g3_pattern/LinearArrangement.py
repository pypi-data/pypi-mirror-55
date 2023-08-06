from pycsp3 import *

n, a = data.n, data.adjacence

# x[i] denotes the 'node' at the i-th position of the stack to be built (primal variables)
x = VarArray(size=n, dom=range(n))

# y[i] denotes the position of the 'node' whose value is i (dual variables)
y = VarArray(size=n, dom=range(n))

# d[i][j] denotes the distance between the ith and jth nodes (if they are adjacent)
d = VarArray(size=[n, n], dom=range(1, n), when=lambda i, j: i < j and a[i][j] == 1)

satisfy(
    AllDifferent(x),

    AllDifferent(y),

    Channel(x, y),

    # Linking primal and distance variables
    [d[i][j] == dist(x[i], x[j]) for i in range(n) for j in range(n) if d[i][j]],

    # triangle constraints: distance(i,j) <= distance(i,k) + distance(k,j)
    # tag(redundant-constraints)
    [d[i][j] <= (d[i][k] if i < k else d[k][i]) + (d[j][k] if j < k else d[k][j]) for i in range(n) for j in range(i + 1, n) if a[i][j] == 1 for k in range(n)
     if a[i][k] == a[j][k] == 1]
)

minimize(
    Sum(d)
)
