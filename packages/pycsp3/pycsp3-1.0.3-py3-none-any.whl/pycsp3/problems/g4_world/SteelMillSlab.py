from pycsp3 import *

orders = data.orders
slabCapacities = sorted(set([0] + data.slabCapacities))
maxCapacity = slabCapacities[-1]
possibleLosses = [min([v for v in slabCapacities if v >= i]) - i for i in range(maxCapacity + 1)]

sizes = [order.size for order in orders]
allColors = sorted(set(order.color for order in orders))
nOrders, nSlabs, nColors = len(orders), len(orders), len(allColors)
colorGroups = [[i for i, order in enumerate(orders) if order.color == color] for color in allColors]

# sb[o] is the slab used to produce order o
sb = VarArray(size=nOrders, dom=range(nSlabs))

# ld[s] is the load of slab s
ld = VarArray(size=nSlabs, dom=range(maxCapacity+1))

# ls[s] is the loss of slab s
ls = VarArray(size=nSlabs, dom=set(possibleLosses))

if not variant():
    satisfy(
        # computing (and checking) the load of each slab
        [Sum([x == s for x in sb] * sizes) == ld[s] for s in range(nSlabs)],

        # computing the loss of each slab 
        [(ld[s], ls[s]) in [(i, loss) for i, loss in enumerate(possibleLosses)] for s in range(nSlabs)],

        # no more than two colors for each slab 
        [Sum(disjunction(sb[o] == s for o in g) for g in colorGroups) <= 2 for s in range(nSlabs)]  # TODO si je fais disjunction()*2 pour tester le xml est mauvais
        # il doit manquer un str quelque part pour les args
    )

elif variant("01"):
    # y[s][o] is 1 iff the slab s is used to produce the order o
    y = VarArray(size=[nSlabs, nOrders], dom={0, 1})
    # z[s][c] is 1 iff the slab s is used to produce an order of color c
    z = VarArray(size=[nSlabs, nColors], dom={0, 1})

    satisfy(
        # linking variables sb and y
        [iff(sb[o] == s, y[s][o]) for s in range(nSlabs) for o in range(nOrders)],

        # linking variables sb and z
        [imply(sb[o] == s, z[s][allColors.index(orders[o].color)]) for s in range(nSlabs) for o in range(nOrders)],

        # computing (and checking) the load of each slab
        [Sum(y[s] * sizes) == ld[s] for s in range(nSlabs)],
        # the reverse side ? eq(z[s]{c] = 1 => or(...) // not really necessary but could help ?

        # computing the loss of each slab
        [(ld[s], ls[s]) in [(i, loss) for i, loss in enumerate(possibleLosses)] for s in range(nSlabs)],

        # no more than two colors for each slab
        [Sum(z[s]) <= 2 for s in range(nSlabs)]

    )

satisfy(
    # tag(redundant-constraints)
    Sum(ld) == sum(sizes),

    # tag(symmetry-breaking)
    [
        Decreasing(ld),

        [sb[i] <= sb[j] for i in range(nOrders) for j in range(i + 1, nOrders) if orders[i].size == orders[j].size and orders[i].color == orders[j].color]
    ]
)


minimize(
    # minimizing summed up loss
    Sum(ls)
)
