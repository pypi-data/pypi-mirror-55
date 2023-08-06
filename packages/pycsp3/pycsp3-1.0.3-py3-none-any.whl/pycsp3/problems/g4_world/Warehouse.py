from pycsp3 import *

cost = data.fixedCost # for each open warehouse
capacities = data.warehouseCapacities
costs = data.storeSupplyCosts
nWarehouses, nStores = len(capacities), len(costs)

# sw[i] is the supplying warehouse for the ith store
sw = VarArray(size=nStores, dom=range(nWarehouses))

# sc[i] is the supplying cost for the ith store
sc = VarArray(size=nStores, dom=lambda i: set(costs[i]))

# open[i] is 1 if the ith warehouse is open
open = VarArray(size=nWarehouses, dom={0, 1})

satisfy(
    # Capacities of warehouses must not be exceeded.
    [Count(sw, value=i) <= capacities[i] for i in range(nWarehouses)],

    # The warehouse supplier of the ith store must be open.
    [open[sw[i]] == 1 for i in range(nStores)],

    # Computing the cost of supplying the ith store.
    [costs[i][sw[i]] == sc[i] for i in range(nStores)]
)

minimize(
    # minimizing the overall cost
    Sum(sc) + Sum(open) * cost
)
