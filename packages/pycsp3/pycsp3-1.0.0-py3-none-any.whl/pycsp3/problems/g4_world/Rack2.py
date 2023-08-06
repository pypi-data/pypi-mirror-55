from pycsp3 import *

nRacks, models, cardTypes = data.nRacks, data.rackModels, data.cardTypes

# we add first a dummy model (0,0,0)
models = [{'power': 0, 'nConnectors': 0, 'price': 0}] + models
nModels, nTypes = len(models), len(cardTypes)

powers, connectors, prices = [model['power'] for model in models], [model['nConnectors'] for model in models], [model['price'] for model in models]
cardPowers = [cardType['power'] for cardType in cardTypes]
maxCapacity = max(connectors)

#  r[i] is the model used for the ith rack
r = VarArray(size=nRacks, dom=range(nModels))

#  c[i][j] is the number of cards of type j put in the ith rack
c = VarArray(size=[nRacks, nTypes], dom=lambda i, j: range(min(maxCapacity, cardTypes[j]['demand'])+1))

# rpw[i] is the power of the ith rack
rpw = VarArray(size=nRacks, dom=set(powers))

# rcn[i] is the number of connectors of the ith rack
rcn = VarArray(size=nRacks, dom=set(connectors))

# rpr[i] is the price of the ith rack
rpr = VarArray(size=nRacks, dom=set(prices))

satisfy(
    # linking the ith rack with its power
    [(r[i], rpw[i]) in enumerate(powers) for i in range(nRacks)],

    # linking the ith rack with its number of connectors
    [(r[i], rcn[i]) in enumerate(connectors) for i in range(nRacks)],

    # linking the ith rack with its price
    [(r[i], rpr[i]) in enumerate(prices) for i in range(nRacks)],

    # connector-capacity constraints
    [Sum(c[i]) <= rcn[i] for i in range(nRacks)],

    # power-capacity constraints
    [Sum(c[i] * cardPowers) <= rpw[i] for i in range(nRacks)],

    # demand constraints
    [Sum(c[ANY, i]) == cardTypes[i]['demand'] for i in range(nTypes)],

    # tag(symmetry-breaking)
    [
        Decreasing(r),
        (r[0] != r[1]) | (c[0][0] >= c[1][0])
    ]
)

minimize(
    Sum(rpr)
)
