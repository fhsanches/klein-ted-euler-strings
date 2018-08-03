#!/usr/bin/env python3

class TreeNode:
    pass

class Arc:
    def __init__(self, s, t, mate=None, label=None): #source, target
        self.s = s
        self.t = t
        if(label == None):
            self.label = generate_label()
        if(mate == None):
            self.mate = self.create_mate()
        else:
            self.mate = mate
            

    def create_mate(self):
        mate = Arc(self.t, self.s, self, self.label+"'")
        return mate

    def euler_visit(self, string):
        res.append(label)
        t.euler(res)
        res.append(mate.label)
        

class Node:    
    def __init__(self, label):
        self.children = []
        self.arcs = []
        self.label = label
    
    def euler(self, res=None):
        if(res == None):
            res = ""
        for arc in self.arcs:
            res.euler_visit(res)
        return res

    def add_child(self, child):
        self.children.append(child)

    def create_arcs(self):
        for node in self.children:
            self.arcs.append(Arc(self, node, node.label))

LABEL_COUNT = 0
def generate_label():
    global LABEL_COUNT
    label = str(LABEL_COUNT)
    LABEL_COUNT += 1
    return label
    


def generate_relevant_substrings(self, F):
    pass

def diff(T, P):
    r = T.root

    if(r.children == None):
        return("")

    v = P[0].t #from top to bottom
    
    p = P[0]
    q = P[0].mate

    E = T.euler()

    T_left = E.split(q)[0]
    T_right = E.split(p)[1]

    res = T_left + T_right + diff(v, v.heavy_path())

    return res


    
        
    
