from pycsp3 import *

visitorGroups = data.visitorGroups  # visitorGroups[i] gives the size of the ith visitor group
visiteeGroups = data.visiteeGroups  # visiteeGroups[i] gives the size of the ith visitee group

nVisitors, nVisitees = sum(visitorGroups), sum(visiteeGroups)
assert nVisitors >= nVisitees, "The number of visitors must be greater than the number of visitees"
n = nVisitors
nDummyVisitees = nVisitors - nVisitees;
if nDummyVisitees > 0:
    visiteeGroups.append(nDummyVisitees)  # a group with dummy visitees is added
nVisitorGroups, nVisiteeGroups = len(visitorGroups), len(visiteeGroups)
nWeeks = len(visitorGroups)

tableForVisitors = [(i, sum(visitorGroups[:i]) + j) for i in range(nVisitorGroups) for j in range(visitorGroups[i])]
tableForVisitees = [(i, sum(visiteeGroups[:i]) + j) for i in range(nVisiteeGroups) for j in range(visiteeGroups[i])]

#  vr[i][w] is the visitor for the ith visitee at week w
vr = VarArray(size=[n, nWeeks], dom=range(n))

#  ve[i][w] is the visitee for the ith visitor at week w
ve = VarArray(size=[n, nWeeks], dom=range(n))

#  gvr[i][w] is the visitor group for the ith visitee at week w
gvr = VarArray(size=[n, nWeeks], dom=range(nVisitorGroups))

#  gve[i][w] is the visitee group for the ith visitor at week w
gve = VarArray(size=[n, nWeeks], dom=range(nVisiteeGroups))

satisfy(
    #  each week, all visitors must be different
    [AllDifferent(col) for col in columns(vr)],

    #  each week, all visitees must be different
    [AllDifferent(col) for col in columns(ve)],

    #  the visitor groups must be different for each visitee
    [AllDifferent(row) for row in gvr],

    #  the visitee groups must be different for each visitor
    [AllDifferent(row) for row in gve],

    #  channeling arrays vr and ve, each week
    [Channel(vr[:, w], ve[:, w]) for w in range(nWeeks)],

    #  tag(symmetry-breaking)
    [
        LexIncreasing(vr, matrix=True),

        [Increasing([vr[i][w] for i in range(nVisitees, n)], strict=True) for w in range(nWeeks)]
    ],

    # linking a visitor with its group
    [(gvr[i][w], vr[i][w]) in tableForVisitors for i in range(n) for w in range(nWeeks)],

    #  linking a visitee with its group
    [(gve[i][w], ve[i][w]) in tableForVisitees for i in range(n) for w in range(nWeeks)]
)
