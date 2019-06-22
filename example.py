#!/usr/bin/env python3

# author: Fernando H. Sanches

from klein import Klein_TED, Cost

t1 = {
    'r':  ['a', 2, 5],
    2: [6]

}

t2 = {
    't': ['b', 2],
    2: [6]
}


# Optional: define your own cdel and cmatch functions
class MyCost(Cost):
    def cdel(self, label):
        if(label == 'a'):
            return 100
        else:
            return 1

    def cmatch(self, label1, label2):
        if(label1 == label2):
            return 0
        else:
            return self.cdel(label1) + 1


mycost = MyCost()
# argument order: tree1, tree2, root1, root2
print(Klein_TED(t1, t2, 'r', 't', mycost))
# return: pair (result, numberOfDistCalls)
