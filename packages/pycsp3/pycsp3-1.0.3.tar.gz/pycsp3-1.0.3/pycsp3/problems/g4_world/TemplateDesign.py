from pycsp3 import *
from math import ceil, floor

nSlots = data.nSlots
demands = data.demands
maxDemand = max(demands)
nVariations = len(demands)
nTemplates = nVariations


def lb(v):
    return ceil(demands[v] * 0.95)


def ub(v):
    return floor(demands[v] * 1.1)


#  d[t][v] is the number of occurrences of variation v on template t
d = VarArray(size=[nTemplates, nVariations], dom=range(nSlots + 1))

#  p[t] is the number of printings of template t
p = VarArray(size=[nTemplates], dom=range(maxDemand + 1))

# u[t] is 1 iff the template t is used
u = VarArray(size=[nTemplates], dom={0, 1})

satisfy(
    #  all slots of all templates are used
    [Sum(d[t]) == nSlots for t in range(nTemplates)],

    #  if a template is used, it is printed at least once
    [iff(u[t] == 1, p[t] > 0) for t in range(nTemplates)]
)

if not variant():
    satisfy(
        # respecting printing bounds for each variation
        Sum(p * d.col(v)) in range(lb(v), ub(v) + 1) for v in range(nVariations)
    )

elif variant("aux"):
    # pv[t][v] is the number of printings of variation v by using template t
    pv = VarArray(size=[nTemplates, nVariations], dom=lambda t, v: range(ub(v)))

    satisfy(
        # linking variables of arrays p and pv
        [p[t] * d[t][v] == pv[t][v] for t in range(nTemplates) for v in range(nVariations)],

        # respecting printing bounds for each variation v
        [Sum(pv.col(v)) in range(lb(v), ub(v) + 1) for v in range(nVariations)]
    )

satisfy(
    # tag(symmetry-breaking)
    [

        [iff(u[t] == 0, d[t][0] == nSlots) for t in range(nTemplates)],

        Decreasing(p),
    ]
)

minimize(
    #  minimizing the number of used templates
    Sum(u)
)
