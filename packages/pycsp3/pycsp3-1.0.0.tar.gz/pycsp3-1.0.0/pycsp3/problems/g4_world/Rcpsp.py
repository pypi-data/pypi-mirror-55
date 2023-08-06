from pycsp3 import *

horizon = data.horizon
resourceCapacities = data.resourceCapacities
jobs = data.jobs
nJobs = len(jobs)


def resource_ctr(j):
    indexes = [i for i in range(nJobs) if jobs[i].requiredQuantities[j] > 0]
    origins = [s[i] for i in indexes]
    lengths = [jobs[i].duration for i in indexes]
    heights = [jobs[i].requiredQuantities[j] for i in indexes]
    return Cumulative(origins=origins, lengths=lengths, heights=heights) <= resourceCapacities[j]


#  s[i] is the starting time of the ith job
s = VarArray(size=nJobs, dom=lambda i: {0} if i == 0 else range(horizon))

satisfy(
    #  precedence constraints
    [s[i] + job.duration <= s[j] for i, job in enumerate(jobs) for j in job.successors],

    # resource constraints
    [resource_ctr(j) for j in range(len(resourceCapacities))]

)

minimize(
    s[- 1]
)
