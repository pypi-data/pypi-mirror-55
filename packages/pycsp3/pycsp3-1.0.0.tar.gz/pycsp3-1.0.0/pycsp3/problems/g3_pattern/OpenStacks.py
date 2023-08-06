from pycsp3 import *

orders = data.orders
n, m = len(orders), len(orders[0])


def table1(i):
    v = sum(orders[i])
    return [(0, 0, 0)] + [(i, ANY, 1) for i in range(1, v)] + [(v, 0, 0), (v, 1, 1)]


def table2(v):
    return [(ANY, i, 0) for i in range(v)] + [(i, ANY, 0) for i in range(v + 1, m)] + [(i, j, 1) for i in range(v + 1) for j in range(v, m)]


if variant("m1"):
    nProducts = [sum(order) for order in orders]

    # p[i] is the ith scheduled product
    p = VarArray(size=m, dom=range(m))

    # np[i][j] is the number of products made at time j and required by customer i
    np = VarArray(size=[n, m], dom=lambda i, j: range(sum(orders[i]) + 1))

    # r[i][j] is 1 iff the product made at time j concerns customer i
    r = VarArray(size=[n, m], dom={0, 1})

    # o[i][j] is 1 iff the stack is open for customer i at time j
    o = VarArray(size=[n, m], dom={0, 1})

    # no[j] is the number of open stacks at time j
    no = VarArray(size=m, dom=range(m + 1))

    satisfy(
        AllDifferent(p),

        [orders[i][p[j]] == r[i][j] for i in range(n) for j in range(m)],

        [np[i][j] == (r[i][j] if j == 0 else np[i][j - 1] + r[i][j]) for i in range(n) for j in range(m)],

        [(np[i][j], r[i][j], o[i][j]) in table1(i) for i in range(n) for j in range(m)],

        [Sum(o[ANY, j]) == no[j] for j in range(m)]
    )

    minimize(
        Maximum(no)
    )

elif variant("m2"):
    # p[i] is the time period of the ith product
    p = VarArray(size=m, dom=range(m))

    # s[i] is the starting time of the stack for the ith product
    s = VarArray(size=n, dom=range(m))

    # e[i] is the ending time of the stack for the ith product
    e = VarArray(size=n, dom=range(m))

    # o[i][j] is 1 iff the stack is open for customer i at time j
    o = VarArray(size=[n, m], dom={0, 1})

    # no[j] is the number of open stacks at time j
    no = VarArray(size=m, dom=range(m + 1))

    satisfy(
        AllDifferent(p),

        [Minimum(p[j] for j in range(m) if orders[i][j] == 1) == s[i] for i in range(n)],

        [Maximum(p[j] for j in range(m) if orders[i][j] == 1) == e[i] for i in range(n)],

        [(s[i], e[i], o[i][j]) in table2(j) for i in range(n) for j in range(m)],

        [Sum(o[ANY, j]) == no[j] for j in range(m)]
    )

    minimize(
        Maximum(no)
    )


    # for ordinary tables : to_ordinary_table(tab, [v + 1, 2, 2]) and to_ordinary_table(tab, [m, m, 2])
