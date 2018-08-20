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
        mate_label = find_mate(self.label)
        mate = Arc(self.t, self.s, mate_label, self)
        return mate

    def euler_visit(self):
        ls = [self.label]
        ls.extend(self.t.E())
        ls.append(self.mate.label)
        return ls


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
        res = []
        for arc in self.arcs:
            res.extend(arc.euler_visit())
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
            return []
        if(not path):
            path = self.heavy_path()
        else:

            v = path[1]  # self's child in P

            p = arcs[(self, v)]
            q = p.mate

            E = self.E()

            T_left = list_split(E, p.label)[0] + [p.label]  # ending with p
            T_right = [q.label] + list_split(E, q.label)[1]  # starting with q

            p = v.heavy_path()
            res = T_left + T_right[::-1] + v.difference_sequence(p)

            return res

    def difference_symbol(self):
        self.difference_sequence()[0]

    def special_subtrees(self):
        hpath = self.heavy_path()
        ls = []
        for node in hpath:
            for child in node.children:
                if(child not in hpath):
                    ls.append(child)
                    ls.extend(child.special_subtrees())

        return ls


class Euler_String():
    '''
    Encapsulates a string and its difference sequence. \
    Overrides access methods to the string
    '''
    def __init__(self, string):
        self._string = string

        self.arcs = [None] * (len(string)+1)

        for (index, character) in enumerate(self._string):
            self.arcs[character] = index

        self.start = 0
        self.end = len(string)

    @property
    def string(self):
        # print("i,j= " + str(self.start) + "," + str(self.end))
        return self._string  # [self.start:self.end]

    def __contains__(self, element):
        return(self.arcs[element])

    def __getitem__(self, index):
        return self._string[index]

    # def __setitem__(self, index, new):
    #     self.string[index] = new
    #     return self.string[index]

    def __str__(self):
        return "<str: " + str(self.string) + ">"

    def index_of(self, item):
        return self.arcs[item]

    def is_empty(self):
        return self.start == self.end

    def substring(self, start, end):
        sub_start = self.start + start
        sub_end = self.start + end
        return Euler_Substring(self, sub_start, sub_end)

    def diffence_symbol(self):
        raise Exception("NYI")

    # vetor        abs   relativo
    # [0, 1, 2, 3] end=4 end=end
    # [0, 1, 2]    end=3 end=parent.end -1
    #    [1, 2]    end=3 end = parent.end
    def remove(self, symbol):
        '''returns new substring without the symbol iff symbol is at an end'''
        print("removing " + str(symbol) + " from " + str(self.string))
        print("with i,j= " + str(self.start) + "," + str(self.end))
        if(self._string[self.start] == symbol):
            return Euler_Substring(self, self.start+1, self.end)
        elif(self._string[self.end-1] == symbol):
            return Euler_Substring(self, self.start, self.end-1)
        else:
            text = "BadRemoval: " + str(symbol) + " from " + str(self.string)
            raise(Exception(text))
        return None

    def has_mate(self, symbol):
        return(symbol*(-1) in self.string)

    def index_of_mate(self, symbol):
        mate = symbol * -1
        return self.arcs[mate]

    def split_first(self, e, is_s=False):
        e_m = find_mate(e)
        mate_index = self.index_of_mate(e)

        (tpp_start, tpp_end) = (self.start+1, mate_index)
        (tp_start, tp_end) = (mate_index + 1, self.end)

        tpp = Euler_Substring(self, tpp_start, tpp_end)
        tp = Euler_Substring(self, tp_start, tp_end)

        return(e, tpp, e_m, tp)

    def split_last(self, e, is_s=False):
        e_m = find_mate(e)
        mate_index = self.index_of_mate(e)

        (tp_start, tp_end) = (self.start, mate_index)
        (tpp_start, tpp_end) = (mate_index + 1, self.end-1)

        tpp = Euler_Substring(self, tpp_start, tpp_end)
        tp = Euler_Substring(self, tp_start, tp_end)

        return(tp, e_m, tpp, e)


class Euler_Substring(Euler_String):
    def __init__(self, parent, start, end):
        self._string = parent._string
        self.parent = parent
        self.start = start
        self.end = end

    @property
    def string(self):
        return self._string[self.start:self.end]

    def __getitem__(self, index):
        print(self._string)
        print("i=" + str(index) +
              ", start= " + str(self.start) +
              ", end= " + str(self.end))

        if(index >= 0):
            return self._string[index+self.start]
        else:
            # index = index * -1
            # index = index + 1
            return self._string[index + self.end]


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
            (ep, spp, epm, sp) = s.split_first(e, True)
        else:
            (tp, em, tpp, e) = t.split_last(e)
            (sp, epm, spp, ep) = s.split_last(e, True)
        return self.dist(sp, tp) + self.dist(spp, tpp) + self.cmatch(e, ep)

    def dist(self, s, t):
        print("dist between s=" + str(s) + " and t=" + str(t))
        return min(self.delete_from_s(s, t),
                   self.delete_from_t(s, t),
                   self.match(s, t))

    def cdel(self, symbol, string):
        print("payed to remove " + str(symbol))
        return 1

    def cmatch(self, symbol1, symbol2):
        print("payed to match " + symbol1 + " with " + symbol2)
        if(symbol1 == symbol2):
            return 0
        return 1


def find_mate(c):
    return c * -1


def list_split(ls, x):
        i = ls.index(x)
        return [ls[0:i], ls[i+1:]]


def is_empty(tup):
    '''input: a tuple'''
    print(tup)
    return tup[0] == tup[1]
