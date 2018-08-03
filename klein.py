#!/usr/bin/env python3

from itertools import chain, imap


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
        self.weigth = 1

    def __iter__(self):
        for v in chain(*imap(iter, self.children)):
            yield v
        yield self

    def euler(self):
        res = ""
        for arc in self.arcs:
            res += arc.euler_visit()
        return res

    def add_child(self, child):
        self.children.append(child)
        arc = Arc(self, child, child.label)
        self.arcs.append(arc)

    def calculate_weigth(self):
        self.weigth = 1
        for child in self.children:
            self.weigth += child.calculate_weigth()
        return self.weigth

    def heavy_child(self):
        heavier_weigth = 0
        heavier_child = None

        for child in self.children:
            child.calculate_weigth()
            if(child.weigth > heavier_weigth):
                (heavier_weigth, heavier_child) = (child.weigth, child)

        return heavier_child

    def post_processing(self):
        self.calculate_weigth()

    def heavy_path(self):
        path = [self]
        node = self.heavy_child()
        while(node is not None):
            path.append(node)
            node = node.heavy_child()

        return path


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
