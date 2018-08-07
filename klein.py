#!/usr/bin/env python3

from itertools import chain, imap

arcs = {}


class Arc:
    def __init__(self, s, t, label=None, mate=None):  # source, target
        self.s = s
        self.t = t
        self.label = label
        if(mate is None):
            self.mate = self.create_mate()
        else:
            self.mate = mate
        arcs[(s, t)] = self

    def create_mate(self):
        mate_label = self.label.upper()
        mate = Arc(self.t, self.s, mate_label, self)
        return mate

    def euler_visit(self):
        return "" + self.label + self.t.E() + self.mate.label


class Node:
    def __init__(self, label):
        self.children = []
        self.arcs = []
        self.label = label
        self.weigth = 1
        self.euler = None

    def __iter__(self):
        for v in chain(*imap(iter, self.children)):
            yield v
        yield self

    def euler_string_compute(self):
        res = ""
        for arc in self.arcs:
            res += arc.euler_visit()
        return res

    def E(self):
        if(not self.euler):
            self.euler = self.euler_string_compute()
        return self.euler

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

    def difference_sequence(self, path=None):
        if(not self.children):  # is empty
            return ""
        if(not path):
            path = self.heavy_path()
        else:

            v = path[1]  # self's child in P

            p = arcs[(self, v)]
            q = p.mate

            E = self.E()

            T_left = E.split(p.label)[0] + p.label  # ending with p
            T_right = q.label + E.split(q.label)[1]  # starting with q

            p = v.heavy_path()
            res = T_left + T_right[::-1] + v.difference_sequence(p)

            print("res = " + res)
            return res

    def difference_symbol(self):
        self.difference_sequence()[0]


class Euler_String():
    def __init__(self, string, difference_sequence):
        self.string = string
        self.diff = difference_sequence

    def __contains__(self, item):
        return(item in self.string)

    def __getiem__(self, item):
        return self.string[item]

    def __setiem__(self, item, new):
        self.string[item] = new
        return self.string[item]

    def is_empty(self):
        return len(self.string) == 0

    def diffence_symbol(self):
        return self.diff[0]

    def remove(self, symbol):
        if(self.string[0] == symbol):
            return self.string[1:]
        elif(self.string[-1] == symbol):
            return self.string[0:-1]
        else:
            raise(Exception("InvalidSymbolRemoval"))
        return None


def generate_relevant_substrings(self, F):
    pass


INFTY = float('inf')


class Klein():
    def delete_from_t(self, s, t):
        if(t.is_empty()):
            return INFTY
        e = t.diffence_symbol()
        if(e.mate.label in t):
            return self.dist(s, t.remove(e)) + self.cdel(e, t)
        else:
            return self.dist(s, t.remove(e))

    def delete_from_s(self, s, t):
        if(not s):
            return INFTY
        if(not t):
            e = s[-1]
        else:
            if(t.diffence_symbol == t.E()[-1]):
                e = s.E()[-1]
            else:
                e = s.E()[0]
        if(e.mate in s.E()):
            return self.dist(s.remove(e), t) + self.cdel(e, s)
        else:
            return self.dist(s.remove(e), t)

    def match(self, s, t):
        if(not s and not t):
            return 0
        if(not s or not t):
            return INFTY
        e = t.diffence_symbol
        if(e == t[0]):
            e_p = s[0]
        else:
            e_p = s[-1]
        if(not (e.mate in t) or not (e_p.mate in s)):
            return INFTY
        if(e == t[0]):
            pass  # TODO

    def dist(self, s, t):
        return min(self.delete_from_s(s, t),
                   self.delete_from_t(s, t),
                   self.match(s, t))

    def cdel(self, symbol, string):
        return 1
