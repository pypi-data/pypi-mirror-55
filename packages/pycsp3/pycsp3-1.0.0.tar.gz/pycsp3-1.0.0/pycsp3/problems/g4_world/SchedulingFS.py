from pycsp3 import *

durations = data.durations  # durations[i][j] is the duration of operation/machine j for job i
n, m = len(durations), len(durations[0])
sumDurations = sum(sum(t) for t in durations)

#  st[i][j] is the start time of the jth operation for the ith job
st = VarArray(size=[n, m], dom=range(sumDurations+1))

# et[i] is the end time of the last operation for the ith job
et = VarArray(size=n, dom=range(sumDurations+1))

satisfy(

    # operations must be ordered on each job
    [Increasing(st[i], lengths=durations[i]) for i in range(n)],

    # computing the end time of each job
    [et[i] == st[i][- 1] + durations[i][- 1] for i in range(n)],

    # no overlap on resources
    [NoOverlap(origins=st[ANY, j], lengths=durations[ANY, j]) for j in range(m)]
)

minimize(
    #  minimizing the makespan
    Maximum(et)
)
