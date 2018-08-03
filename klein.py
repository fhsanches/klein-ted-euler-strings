#!/usr/bin/env python3


class Arc:
    def __init__(self, s, t, label=None, mate=None):  # source, target
        self.s = s
        self.t = t
        self.label = label
        if(mate is None):
            self.mate = self.create_mate()
        else:
            self.mate = mate

    def create_mate(self):
        mate = Arc(self.t, self.s, self.label+"'", self)
        return mate

    def euler_visit(self):
        return "" + self.label + self.t.euler() + self.mate.label


class Node:
    def __init__(self, label):
        self.children = []
        self.arcs = []
        self.label = label

    def euler(self):
        res = ""
        for arc in self.arcs:
            res += arc.euler_visit()
        return res

    def add_child(self, child):
        self.children.append(child)
        arc = Arc(self, child, child.label)
        self.arcs.append(arc)


class Labeler():
    def __init__(self):
        self.count = 0

    def generate_label(self):
        label = str(self.count)
        self.count += 1
        return label


def generate_relevant_substrings(self, F):
    pass


def diff(T, P):
    r = T.root

    if(r.children is None):
        return("")

    v = P[0].t  # from top to bottom

    p = P[0]
    q = P[0].mate

    E = T.euler()

    T_left = E.split(q)[0]
    T_right = E.split(p)[1]

    res = T_left + T_right + diff(v, v.heavy_path())

    return res
