#!/usr/bin/env python3

from itertools import chain, imap

arcs = {}


class Arc:
    def __init__(self, s, t, label=None, mate=None):  # source, target
        '''
        initializes arc, creates mate (if not given), add self to "arcs" dict
        '''
        self.s = s
        self.t = t
        self.label = label
        if(mate is None):
            self.mate = self.create_mate()
        else:
            self.mate = mate
        arcs[(s, t)] = self

    def create_mate(self):
        mate_label = string_mate(self.label)
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

            #print("res = " + res)
            return res

    def difference_symbol(self):
        self.difference_sequence()[0]


class Euler_String():
    '''
    Encapsulates a string and its difference sequence. \
    Overides access methods to the string
    '''
    def __init__(self, string, difference_sequence):
        self.string = string
        self.diff = difference_sequence

    def __contains__(self, index):
        return(index in self.string)

    def __getitem__(self, index):
        print("str = " + self.string + "/index = " + str(index))
        return self.string[index]

    def __setiem__(self, index, new):
        self.string[index] = new
        return self.string[index]

    def __str__(self):
        return "<str: " + self.string + "/diff: " + self.diff + ">"

    def find(self, item):
        result = str(self.string.find(item))
        print("finding " + item + " in " + self.string + ":" + result)
        return(self.string.find(item) >= 0)

    def is_empty(self):
        #  print("len = " + str(len(self.string)))
        return len(self.string) == 0

    def diffence_symbol(self):
        return self.diff[0]

    def remove(self, symbol):
        '''returns a new string without symbol, if symbol is at an end'''
        print("removing " + symbol + " from " + self.string)
        if(self.string[0] == symbol):
            return Euler_String(self.string[1:], self.diff[1:])
        elif(self.string[-1] == symbol):
            return Euler_String(self.string[:-1], self.diff[1:])
        else:
            raise(Exception("BadRemoval: " + symbol + " from " + self.string))
        return None

    def has_mate(self, symbol):
        mate = string_mate(symbol)
        return(mate in self.string)

    def split_first(self, e):
        em = string_mate(e)
        newdiff = self.diff[1:]

        es = self.string.split(em)

        newdiff = newdiff.split(em)

        print("splitting " + str(self) + "at " + em)
        print("es= " + str(es) + " diff= " + str(newdiff))
        tpp = Euler_String(es[0][1:], newdiff[0])

        if(len(newdiff) == 1):  # I'm dealing with s, it's fine to break diff
            tp = Euler_String(es[1], newdiff[0])
        else:
            tp = Euler_String(es[1], newdiff[1])

        return(e, tpp, em, tp)

    def split_last(self, e):
        em = string_mate(e)
        es = self.string.split(em)
        newdiff = self.diff[1:]

        print("splitting " + str(self) + "at " + em)
        print("es= " + str(es) + " diff= " + str(newdiff))

        tp = Euler_String(es[0], newdiff[0])
        tpp = Euler_String(es[1][:-1], newdiff[1:])

        if(len(newdiff) == 1):  # I'm dealing with s, it's fine to break diff
            tp = Euler_String(es[1], newdiff[0])
        else:
            tp = Euler_String(es[1], newdiff[1])

        return(tp, em, tpp, e)


def generate_relevant_substrings(self, F):
    pass


INFTY = float('inf')


class Klein():
    def delete_from_t(self, s, t):
        if(t.is_empty()):
            return INFTY
        e = t.diffence_symbol()
        if(t.has_mate(e)):
            return(self.dist(s, t.remove(e)) + self.cdel(e, t))
        else:
            return(self.dist(s, t.remove(e)))

    def delete_from_s(self, s, t):
        if(s.is_empty()):
            return INFTY
        if(t.is_empty()):
            e = s[-1]
        else:
            if(t.diffence_symbol() == t[-1]):
                e = s[-1]
            else:
                e = s[0]
        if(s.has_mate(e)):
            return self.dist(s.remove(e), t) + self.cdel(e, s)
        else:
            return self.dist(s.remove(e), t)

    def match(self, s, t):
        print("match s=" + str(s) + " t=" + str(t))
        if(s.is_empty() and t.is_empty()):
            return 0
        if(s.is_empty() or t.is_empty()):
            return INFTY
        e = t.diffence_symbol()
        if(e == t[0]):
            e_p = s[0]
        else:
            e_p = s[-1]
        if((not t.has_mate(e)) or (not s.has_mate(e_p))):
            return INFTY
        if(e == t[0]):
            (e, tpp, em, tp) = t.split_first(e)
            (ep, spp, epm, sp) = s.split_first(e)
        else:
            (tp, em, tpp, e) = t.split_last(e)
            (sp, epm, spp, ep) = s.split_last(e)
        return self.dist(sp, tp) + self.dist(spp, tpp) + self.cmatch(e, ep)

    def dist(self, s, t):
        print("dist between " + str(s) + " and " + str(t))
        return min(self.delete_from_s(s, t),
                   self.delete_from_t(s, t),
                   self.match(s, t))

    def cdel(self, symbol, string):
        print("payed to remove " + symbol)
        return 1

    def cmatch(self, symbol1, symbol2):
        print("payed to match " + symbol1 + " with " + symbol2)
        if(symbol1 == symbol2):
            return 0
        return 1


def string_mate(c):
    if(c.islower()):
        return c.upper()
    else:
        return c.lower()
