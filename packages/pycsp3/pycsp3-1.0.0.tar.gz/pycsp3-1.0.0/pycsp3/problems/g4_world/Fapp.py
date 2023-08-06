from pycsp3 import *

from multiprocessing import cpu_count, Pool

from pycsp3.tools.curser import OpOverrider

domains, routes = data.domains, data.routes
n = len(routes)
hards, softs = data.hards, data.softs
nHards, nSofts = len(hards) if hards else 0, len(softs)


def frequency_domain(i):
    return set(domains[routes[i].domain])


def polarization_domain(i):
    return {0, 1} if routes[i].polarization == 0 else {1} if routes[i].polarization == 1 else {0}


def calculate_size(t, k, distance):
    size = 0
    for l in range(k - 1):
        if distance < t[l]:
            size += 1
    return size


def table_relaxable_link(i, c):
    OpOverrider.disable()
    # print("Parallel table creation in progress: " + str(i)+"/"+str(nSofts))
    dom1, dom2 = routes[c.route1].domain, routes[c.route2].domain
    pol1, pol2 = routes[c.route1].polarization, routes[c.route2].polarization
    table = []
    for f1 in domains[dom1]:
        for f2 in domains[dom2]:
            distance = abs(f1 - f2)
            for pol in range(4):
                p1 = 0 if pol < 2 else 1
                p2 = 1 if (pol == 1 or pol == 3) else 0
                if (pol1 == 1 and p1 == 0) or \
                        (pol1 == -1 and p1 == 1) or \
                        (pol2 == 1 and p2 == 0) or \
                        (pol2 == -1 and p2 == 1):
                    continue
                t = c.eqRelaxations if p1 == p2 else c.neRelaxations
                for k in range(12):
                    if k == 11 or distance >= t[k]:  # for k=11, we suppose t[k] = 0
                        table.append((f1, f2, p1, p2, k,
                                      0 if k == 0 or distance >= t[k - 1] else 1,
                                      0 if k <= 1 else calculate_size(t, k, distance)))

    OpOverrider.enable()
    return table


def table_relaxable_link_short(i, c):
    OpOverrider.disable()
    # print("Parallel table creation in progress: " + str(i)+"/"+str(nSofts))
    dom1, dom2 = routes[c.route1].domain, routes[c.route2].domain
    pol1, pol2 = routes[c.route1].polarization, routes[c.route2].polarization
    set_short_version = set()
    table = []
    for f1 in domains[dom1]:
        for f2 in domains[dom2]:
            distance = abs(f1 - f2)
            if distance in set_short_version:
                continue
            for pol in range(4):
                p1 = 0 if pol < 2 else 1
                p2 = 1 if (pol == 1 or pol == 3) else 0
                if (pol1 == 1 and p1 == 0) or (pol1 == -1 and p1 == 1) or (pol2 == 1 and p2 == 0) or (pol2 == -1 and p2 == 1):
                    continue
                t = c.eqRelaxations if p1 == p2 else c.neRelaxations
                for k in range(12):
                    if k == 11 or distance >= t[k]:  # for k=11, we suppose t[k] = 0
                        table.append((distance, p1, p2, k, 0 if k == 0 or distance >= t[k - 1] else 1,
                                      0 if k <= 1 else calculate_size(t, k, distance)))
    
    OpOverrider.enable()
    return table


def parallel_create_table(short=False):
    print("Parallel table creation in progress ...")
    pool = Pool(processes=cpu_count())
    result_objects = [pool.apply_async(table_relaxable_link if not short else table_relaxable_link_short,
                                       args=(i, c)) for i, c in enumerate(softs)]
    results = [r.get() for r in result_objects]
    pool.close()
    pool.join()
    print("Parallel table creation finished")
    return results


def distances(i, j):
    dom1, dom2 = domains[routes[i].domain], domains[routes[j].domain]
    return {abs(f1 - f2) for f1 in dom1 for f2 in dom2}


def soft_links():
    t = [[False] * n for _ in range(n)]
    for c in softs:
        i, j = c.route1, c.route2
        t[i][j] = True
        t[j][i] = True
    return t


def imperative(c):
    i, j = c.route1, c.route2
    if c.frequency:
        if c.gap == 0:
            return f[i] == f[j] if c.equality else f[i] != f[j]
        return dist(f[i], f[j]) == c.gap if c.equality else dist(f[i], f[j]) != c.gap
    return p[i] == p[j] if c.equality else p[i] != p[j]


softLinks = soft_links()  # used by model m2 (not currently implemented)

#  f[i] is the frequency of the ith radio-link
f = VarArray(size=[n], dom=frequency_domain)

#  p[i] is the polarization of the ith radio-link
p = VarArray(size=[n], dom=polarization_domain)

# k is the relaxation level to be optimized
k = Var(dom=range(12))

#  v1[q] is 1 iff the qth pair of radio-electric compatibility constraints is violated when relaxing another level
v1 = VarArray(size=[nSofts], dom={0, 1})

#  v2[q] is the number of times the qth pair of radio-electric compatibility constraints is violated when relaxing more than one level
v2 = VarArray(size=[nSofts], dom=range(11))

satisfy(
    # imperative constraints
    [imperative(h) for h in hards]
)
    
# To speed up the calculation
for element in softs:
    element['neRelaxations'] = tuple(element['neRelaxations'])
    element['eqRelaxations'] = tuple(element['eqRelaxations'])

    
if not variant():
    satisfy(
        # relaxable radio-electric compatibility constraints
        (f[softs[i].route1], f[softs[i].route2], p[softs[i].route1], p[softs[i].route2], k, v1[i], v2[i]) in table
        for i, table in enumerate(parallel_create_table())

        # (f[c.route1], f[c.route2], p[c.route1], p[c.route2], k, v1[i], v2[i]) in table_relaxable_link(i, c) for i, c in enumerate(softs)
    )

elif variant("short"):
    # d[i][j] is the distance between the ith and the jth frequencies (for i < j when a soft link exists)
    d = VarArray(size=[n, n], dom=lambda i, j: distances(i, j), when=lambda i, j: i < j and softLinks[i][j])

    satisfy(

        # computing intermediary distances
        [d[i][j] == dist(f[i], f[j]) for i in range(n) for j in range(i + 1, n) if softLinks[i][j]],

        # relaxable radio-electric compatibility constraints
        [((d[softs[i].route1][softs[i].route2] if softs[i].route1 < softs[i].route2 else d[softs[i].route2][softs[i].route1]),
          p[softs[i].route1], p[softs[i].route2], k, v1[i], v2[i]) in table
         for i, table in enumerate(parallel_create_table(True))]

    )

minimize(
    k * (10 * nSofts ** 2) + Sum(v1) * (10 * nSofts) + Sum(v2)
)

#
