from pycsp3 import *

jobs = data.jobs

n, m = len(jobs), len(jobs[0].durations)
sumDurations = sum(sum(j.durations) for j in jobs)
maxTime = max(j.dueDate for j in jobs) if all(j.dueDate != -1 for j in jobs) else sumDurations

#  st[i][j] is the start time of the jth operation for the ith job
st = VarArray(size=[n, m], dom=range(maxTime))

#  et[i] is the end time of the last operation for the ith job
et = VarArray(size=[n], dom=range(maxTime))


def respecting_dates(i):
    if jobs[i].releaseDate > 0:
        return st[i][0] > jobs[i].releaseDate
    if jobs[i].dueDate != -1 and jobs[i].dueDate < maxTime - 1:
        return et[i] <= jobs[i].dueDate
    return None


satisfy(
    # operations must be ordered on each job
    [Increasing(st[i], lengths=jobs[i].durations) for i in range(n)],

    # computing the end time of each job
    [et[i] == st[i][m - 1] + jobs[i].durations[m - 1] for i in range(n)],

    # respecting release and due dates
    [respecting_dates(i) for i in range(n)],

    #  no overlap on resources
    [NoOverlap(origins=[st[i][jobs[i].resources.index(j)] for i in range(m)], lengths=[jobs[i].durations[jobs[i].resources.index(j)] for i in range(m)])
     for j in range(m)]
)

minimize(
    # minimizing the makespan
    Maximum(et)
)
