from pycsp3 import *

rsums, csums = data.rowSums, data.colSums
n = len(csums)
sizes, occurrences = [ship.size for ship in data.fleet], [ship.size * ship.cnt for ship in data.fleet]
maxOccurrence = max(occurrences)
hints = data.hints if data.hints else []
pos, neg = sizes, [-v for v in sizes]


def automaton(hor):
    def q(i, j=None):
        return "q" + str(i) + ("" if j is None else "x" + str(j))

    transitions = [(q(0), 0, q(0)), (q(0), neg if hor else pos, "qq"), ("qq", 0, q(0))]
    for i in (pos if hor else neg):
        transitions += [(q(0), i, q(abs(i), 1))] + [(q(abs(i), j), i, q(abs(i), j + 1)) for j in range(1, abs(i))] + [(q(abs(i), abs(i)), 0, q(0))]
    return Automaton(start=q(0), final=q(0), transitions=transitions)


table = [(0, ANY, ANY, ANY, ANY), (1, 0, 0, 0, 0)]
ah, av = automaton(True), automaton(False)  # automata for ships online

#  s[i][j] is 1 iff the cell at row i and col j is occupied by a ship segment
s = VarArray(size=[n + 2, n + 2], dom={0, 1})

# t[i][j] is 0 iff the cell at row i and col j is inoccupied, the type (size) of the ship fragment otherwise,
# when positive, the ship is put horizontally, when negative, the ship is put vertically
t = VarArray(size=[n + 2, n + 2], dom=neg + [0] + pos)  # set(pos) | {0} | set(neg))

# cp[i] is the number of positive ship segments of type i
cp = VarArray(size=len(pos), dom=range(maxOccurrence + 1))

# cn[i] is the number of negative ship segments of type i
cn = VarArray(size=len(neg), dom=lambda i: {0} if neg[i] == -1 else range(maxOccurrence + 1))

scp = [t[i][j] for i in range(1, n + 1) for j in range(1, n + 1)]


def hint_ctr(hint):
    i, j, c = hint.row, hint.col, hint.type[0];
    if c == 'w':
        return s[i][j] == 0
    if c in {'c', 'l', 'r', 't', 'b'}:
        return [
            s[i][j] == 1,
            s[i - 1][j] == (1 if c == 'b' else 0),
            s[i + 1][j] == (1 if c == 't' else 0),
            s[i][j - 1] == (1 if c == 'r' else 0),
            s[i][j + 1] == (1 if c == 'l' else 0)
        ]
    if c == 'm':
        return [
            s[i][j] == 1,
            t[i][j] not in {-2, -1, 0, 1, 2},
            (s[i - 1][j], s[i + 1][j], s[i][j - 1], s[i][j + 1]) in [(0, 0, 1, 1), (1, 1, 0, 0)]
        ]


satisfy(
    # no ship on borders
    [
        [Sum(s[0]) == 0,
         Sum(s[n + 1]) == 0,
         Sum(s.col(0)) == 0,
         Sum(s.col(n + 1)) == 0]
    ],

    # respecting the specified row and column tallies
    [
        [Sum(s[i + 1]) == rsums[i] for i in range(n)],
        [Sum(s.col(j + 1)) == csums[j] for j in range(n)]
    ],

    #  being careful about cells on diagonals
    [(s[i][j], s[i - 1][j - 1], s[i - 1][j + 1], s[i + 1][j + 1], s[i + 1][j - 1]) in table for i in range(1, n + 1) for j in range(1, n + 1)],

    # tag(channeling)
    [iff(s[i][j] == 1, t[i][j] != 0) for i in range(n + 2) for j in range(n + 2)],

    #  ensuring the right number of occurrences of ship segments of each type
    [
        [Count(scp, value=pos[i]) == cp[i] for i in range(len(sizes))],
        [Count(scp, value=neg[i]) == cn[i] for i in range(len(sizes))],
        [cp[i] + cn[i] == occurrences[i] for i in range(len(sizes))]
    ],

    # ensuring connexity of ship segments
    [
        [t[i] in ah for i in range(1, n + 1)],
        [t.col(j) in av for j in range(1, n + 1)]
    ],

    # tag(clues)
    [hint_ctr(hint) for hint in hints]
)

# TODO cardinality a la place des count ?  (chriss)
