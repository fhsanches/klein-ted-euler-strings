#!/usr/bin/env python3
from klein import Klein_TED

t1 = {
    'r':  ['a', 2, 5],
    2: [6]

}

t2 = {
    't': ['b', 2],
    2: [6]
}


# argument order: tree1, tree2, root1, root2
print(Klein_TED(t1, t2, 'r', 't'))
