from pycsp3 import *

nPlayers = data.nPlayers
leagueSize = data.leagueSize
playerRankings, playerCountries = data.playerRankings, data.playerCountries

nLeagues = nPlayers // leagueSize + (1 if nPlayers % leagueSize != 0 else 0)
nFullLeagues = nLeagues if nPlayers % leagueSize == 0 else nLeagues - (leagueSize - nPlayers % leagueSize)
allRankings, allCountries = set(playerRankings), set(playerCountries)
nCountries = len(allCountries)

table1 = [(i, playerRankings[i], playerCountries[i]) for i in range(nPlayers)]
table2 = [tuple([i, playerRankings[i]] + [1 if j - 2 + 1 == playerCountries[i] else ANY for j in range(2, 2 + nCountries)]) for i in range(nPlayers)]

lp = VarArray(size=[nLeagues, leagueSize], dom=range(nPlayers), when=lambda l, k: l < nFullLeagues or k < leagueSize - 1)

rlp = VarArray(size=[nLeagues, leagueSize], dom=allRankings, when=lambda l, k: l < nFullLeagues or k < leagueSize - 1)

minrlp = VarArray(size=nLeagues, dom=allRankings)

maxrlp = VarArray(size=nLeagues, dom=allRankings)

diffrlp = VarArray(size=nLeagues, dom={0} | allRankings)

nc = VarArray(size=nLeagues, dom=lambda l: range(1 + min(nCountries, leagueSize if l < nFullLeagues else leagueSize - 1)))

satisfy(
    AllDifferent(lp),

    [Minimum(rlp[i]) == minrlp[i] for i in range(nLeagues)],

    [Maximum(rlp[i]) == maxrlp[i] for i in range(nLeagues)],

    [diffrlp[i] == maxrlp[i] - minrlp[i] for i in range(nLeagues)]
)

if not variant():
    clp = VarArray(size=[nLeagues, leagueSize], dom=allCountries, when=lambda l, k: l < nFullLeagues or k < leagueSize - 1)

    satisfy(
        [(lp[l][k], rlp[l][k], clp[l][k]) in table1 for l in range(nLeagues) for k in range(leagueSize) if l < nFullLeagues or k < leagueSize - 1],

        [Nvalues(clp[l]) == nc[l] for l in range(nLeagues)]
    )

elif variant("01"):  # TODO not sure that this variant is correct
    clc = VarArray(size=[nLeagues, nCountries], dom={0, 1})

    satisfy(
        [(lp[l][k], rlp[l][k], clc[l]) in table2 for l in range(nLeagues) for k in range(leagueSize) if l < nFullLeagues or k < leagueSize - 1],

        [imply(clc[l][c] == 0, lp[l][k] != i) for (l, k, c, i) in product(range(nLeagues), range(leagueSize), range(nCountries), range(nPlayers))
         if (l < nFullLeagues or k < leagueSize - 1) and playerCountries[i] == c + 1],

        [Sum(clc[l]) == nc[l] for l in range(nLeagues)]
    )

minimize(
    Sum(diffrlp) * 100 - Sum(nc)
)

# Sum(x * 100 for x in diffrlp) + Sum(-x for x in nc)
# Sum(x * 100 for x in diffrlp) + Sum(x * -1 for x in nc)
# Sum((diffrlp + nc) * ([100] * nLeagues + [-1] * nLeagues))
# diffrlp * ([100] * nLeagues) + nc * ([-1] * nLeagues)
