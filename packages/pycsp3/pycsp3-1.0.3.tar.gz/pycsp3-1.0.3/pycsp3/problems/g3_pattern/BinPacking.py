from pycsp3 import *


def n_bins():
    cnt = 0
    curr_load = 0
    for i, weight in enumerate(weights):
        curr_load += weight
        if curr_load > capacity:
            cnt += 1
            curr_load = weight
    return cnt


def max_items_per_bin():
    curr = 0
    for i, weight in enumerate(weights):
        curr += weight
        if curr > capacity:
            return i
    return -1


def occurrences_of_weights():
    pairs = []
    cnt = 1
    for i in range(1, len(weights)):
        if weights[i] != weights[i - 1]:
            pairs.append((weights[i - 1], cnt))
            cnt = 0
        cnt += 1
    pairs.append((weights[-1], cnt))
    return pairs


def table_recursive(tuples, n_stored, tmp, i, curr):
    if len(tuples) > 200000000:
        return False
    assert curr + weights[i] <= capacity
    tmp[n_stored] = weights[i]
    n_stored += 1
    curr += weights[i]
    tuples.append(tuple(tmp[j] if j < n_stored else 0 for j in range(len(tmp))))
    for j in range(i):
        if curr + weights[j] > capacity:
            break
        if j < i - 1 and weights[j] == weights[j + 1]:
            continue
        if not table_recursive(tuples, n_stored, tmp, j, curr):
            return False
    return True


def table():
    tuples = []
    tmp = [0] * maxPerBin
    tuples.append(tuple(tmp.copy()))
    for i in range(len(weights)):
        if i < len(weights) - 1 and weights[i] == weights[i + 1]:
            continue
        if not table_recursive(tuples, 0, tmp, i, 0):
            raise Exception("not possible to build the table with less than the specified number of tuples")
    return tuples


capacity = data.binCapacity
weights = sorted(data.itemWeights)
nItems, nBins, maxPerBin = len(weights), n_bins(), max_items_per_bin()

# x is the number of unused bins
x = Var(dom=range(nBins + 1))

# b[i][j] indicates the weight of the jth object put in the ith bin. It is 0 if there is no object at this place.
b = VarArray(size=[nBins, maxPerBin], dom={0, *weights})

if not variant():
    satisfy(
        [Sum(b[i]) <= capacity for i in range(nBins)],

        [Decreasing(b[i]) for i in range(nBins)]
    )

elif variant("table"):
    table = table()
    satisfy(
        b[i] in table for i in range(nBins)
    )

satisfy(
    Cardinality(b, occurrences={0: nBins * maxPerBin - nItems} + {weight: occ for (weight, occ) in occurrences_of_weights()}),

    # tag(symmetry-breaking)
    LexDecreasing(b),

    Count(b[ANY, 0], value=0) == x
)

maximize(x)
