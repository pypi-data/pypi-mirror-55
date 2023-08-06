from pycsp3 import *

nPeriods = data.nPeriods
boats = data.boats
nBoats = len(boats)
crewSizes = [boat.crewSize for boat in boats]

# h[b] indicates if the boat b is a host boat
h = VarArray(size=nBoats, dom={0, 1})

# s[b][p] is the boat b' where the crew of boat b is at period p
s = VarArray(size=[nBoats, nPeriods], dom=range(nBoats))

# g[b1][p][b2] is 1 if s[b1][p] = b2
g = VarArray(size=[nBoats, nPeriods, nBoats], dom={0, 1})

# e[b1][b2][p] is 1 if s[b1][p] = s[b2][p]
e = VarArray(size=[nBoats, nBoats, nPeriods], dom={0, 1}, when=lambda b1, b2, p: b1 < b2)

satisfy(
    [iff(h[b], s[b][p] == b) for b in range(nBoats) for p in range(nPeriods)],

    [imply(s[b1][p] == b2, h[b2]) for b1 in range(nBoats) for p in range(nPeriods) for b2 in range(nBoats) if b1 != b2],

    [Channel(g[b][p], s[b][p]) for b in range(nBoats) for p in range(nPeriods)],

    [Sum(g[ANY, p, b] * crewSizes) <= boats[b].capacity for b in range(nBoats) for p in range(nPeriods)],

    [AllDifferent(s[b], excepting=b) for b in range(nBoats)],

    [iff(e[b1][b2][p], s[b1][p] == s[b2][p]) for b1 in range(nBoats) for b2 in range(b1 + 1, nBoats) for p in range(nPeriods)],

    [Sum(e[b1][b2]) <= 2 for b1 in range(nBoats) for b2 in range(b1 + 1, nBoats)]
)

minimize(
    Sum(h)
)


# less compact way of posting : [Sum([g[i][p][b] for i in range(nBoats)] * crewSizes) <= boats[b].capacity for b in range(nBoats) for p in range(nPeriods)],
