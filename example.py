#!/usr/bin/env python3

from klein import Klein_TED

t1 = {
        1: [2, 3],
        2: [4],
        4: [5],
}

t2 = {
        1: [2, 3],
        2: [5],
        3: [4],
}


print(Klein_TED(t1,t2))
