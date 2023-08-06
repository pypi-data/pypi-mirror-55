import math

from pycsp3 import *

"""
    Rectangle packing problem. See Simonis and O'Sullivan. Search strategies for rectangle packing. 
    In Proceedings of CP 2008. Also used in short supports papers."
"""

container = data.container
boxes = data.boxes
nRectangles = len(boxes)

# x[i] is the x-coordinate where is put the ith rectangle
x = VarArray(size=nRectangles, dom=range(container.width))

# y[i] is the y-coordinate where is put the ith rectangle
y = VarArray(size=nRectangles, dom=range(container.height))

satisfy(
    #  unary constraints on x
    [x[i] + boxes[i].width <= container.width for i in range(nRectangles)],

    # unary constraints on y
    [y[i] + boxes[i].height <= container.height for i in range(nRectangles)],

    NoOverlap(origins=[(x[i], y[i]) for i in range(nRectangles)], lengths=[(boxes[i].width, boxes[i].height) for i in range(nRectangles)])

)

if container.width == container.height:
    satisfy(
        # tag(symmetry-breaking)
        [
            x[nRectangles - 1] <= math.floor((container.width - boxes[nRectangles - 1].width) // 2.0),

            y[nRectangles - 1] <= x[nRectangles - 1]
        ]
    )
