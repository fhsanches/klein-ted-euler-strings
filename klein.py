#!/usr/bin/env python3

from itertools import chain, imap

INFTY = float('inf')


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
        s.arcs_dict[(s.label, t.label)] = self

    def create_mate(self):
        mate_label = find_mate(self.label)
        mate = Arc(self.t, self.s, mate_label, self)
        return mate

    def euler_visit(self):
        ls = [self.label]
        ls.extend(self.t.euler_visit())
        ls.append(self.mate.label)
        # ls.extend(self.t.E())
        # ls.append(self.mate.label)
        return ls


class Node:
    def __init__(self, label, tree_root=None):
        self.children = []
        self.arcs = []
        self.label = label
        self.weigth = 1
        self.euler = None
        self.root = None
        if(not tree_root):
            self.arcs_dict = {}
        else:
            self.arcs_dict = tree_root.arcs_dict

    def __iter__(self):
        for v in chain(*imap(iter, self.children)):
            yield v
        yield self

    def euler_list_compute(self):
        res = []
        for arc in self.arcs:
            res.append(arc.label)
            res.extend(arc.t.euler_list_compute())
        return res

    def E(self):
        if(not self.euler):
            el = self.euler_list_compute()
            self.euler = Euler_String(el)
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

    def post_processing(self, root):
        self.calculate_weigth()
        self.set_roots(self)

    def set_roots(self, root):
        self.root = root
        for child in self.children:
            child.set_roots(root)

    def heavy_path(self):
        path = [self]
        node = self.heavy_child()
        while(node is not None):
            path.append(node)
            node = node.heavy_child()

        return path

    def difference_sequence(self, E, pos, path):
        if(not self.children):  # is empty
            return []
        if(not path):
            path = self.heavy_path()
        else:
            (st, ed) = pos

            v = path[1]  # self's child in P

            p = self.arcs_dict[(self, v)]
            q = p.mate

            rv = E.arcs[p.label]
            vr = E.arcs[q.label]

            T_left = E[st:rv]  # ending with p
            T_right = E[vr:ed]  # starting with p

            print(p.label)
            print(q.label)
            print("rv = " + str(rv) + " vr = " + str(vr))
            print("T_left = " + str(T_left))
            print("T_right = " + str(T_right))

            # T_left = list_split(E, p.label)[0] + [p.label]  # ending with p
            # T_right = [q.label] +list_split(E, q.label)[1]  # starting with q

            p = v.heavy_path()
            res = T_left + T_right[::-1] + v.difference_sequence(
                E, pos, path)

            self.difference_seq = res

            return res

    def set_diff_dict(self):
        diff = {}
        euler = self.root.E()
        i = 1
        j = len(euler)

        seq = self.difference_sequence()

        for label in seq:
            if(label == euler[i]):
                diff[(i, j)] = 0
                i += 1
            elif(label == euler[j]):
                diff[(i, j)] = -1
                j -= 1
            else:
                raise Exception("Bad difference sequence")

            euler.diff_dict = diff
        # a

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
        self.string = string

        self.arcs = [None] * (len(string)*20+1)  # fixme esse *2 e' gambiarra
        print("str= " + str(string))
        print(self.arcs)

        for (index, value) in enumerate(self.string):
            print(value)
            self.arcs[value] = index

        self.start = 0
        self.end = len(string)

        # self._difference_darts = {}
        self.diff_dict = {}
        self.diff_seq = None

    def get_pos(self):
        return(self.start, self.end)

    def __str__(self):
        return "<str: " + str(self.string) + ">"

    def __getitem__(self, index):
        return self.string[index]

    def diffence_symbol(self, pos):
        (start, end) = pos
        try:
            x = self.diff_dict[(start, end)]
        except Exception:
            print("dict=" + str(self.diff_dict))
            x = None
            raise(Exception("BadDictAccess"))
        return x

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

        tpp = (tpp_start, tpp_end)
        tp = (tp_start, tp_end)

        return(e, tpp, e_m, tp)

    def split_last(self, e, is_s=False):
        e_m = find_mate(e)
        mate_index = self.index_of_mate(e)

        (tp_start, tp_end) = (self.start, mate_index)
        (tpp_start, tpp_end) = (mate_index + 1, self.end-1)

        tpp = (tpp_start, tpp_end)
        tp = (tp_start, tp_end)

        return(tp, e_m, tpp, e)

    def build_diff_dict(self, pos):
        if(not self.diff_seq):
            self.difference_sequence()

        i = self.start
        j = self.end - 1

        for element in self.difference_seq:
            element_pos = self.arcs[element]
            if(element_pos == i):
                self.diff_dict[(i, j)] = True
            elif(element_pos == j):
                self.diff_dict[(i, j)] = False
            else:
                raise Exception("Bad difference sequence")

    def remove(self, pos, symbol):
        '''returns new substring without the symbol iff symbol is at an end'''
        (start, end) = pos
        if(self[start] == symbol):
            return (start+1, end)
        elif(self[end-1] == symbol):
            return (start, end-1)
        else:
            text = "BadRemoval: " + str(symbol) + " from " + str(self)
            raise(Exception(text))
        return None

    def substring(self, parent, start, end):
        sub_start = parent.start + start
        sub_end = parent.start + end
        return (sub_start, sub_end)

    def is_empty(self, pos):
        (st, ed) = pos
        return (st == ed)


class Klein():
    def delete_from_t(self, s, s_pos, t, t_pos):
        if(t.is_empty(t_pos)):
            return INFTY
        e = t.diffence_symbol(t_pos)
        if(t.has_mate(e)):
            return(self.dist(s, t.remove(t_pos, e)) + self.cdel(e, t))
        else:
            return(self.dist(s, t.remove(t_pos, e)))

    def delete_from_s(self, s, s_pos, t, t_pos):
        if(s.is_empty(s_pos)):
            return INFTY
        if(t.is_empty(t_pos)):
            e = s[-1]
        else:
            if(t.diffence_symbol(t_pos) == t[-1]):
                e = s[-1]
            else:
                e = s[0]
        if(s.has_mate(e)):
            return self.dist(s.remove(e), t) + self.cdel(e, s)
        else:
            return self.dist(s.remove(e), t)

    def match(self, s, s_pos, t, t_pos):
        print("match s=" + str(s) + " t=" + str(t))
        if(s.is_empty(s_pos) and t.is_empty(t_pos)):
            return 0
        if(s.is_empty(s_pos) or t.is_empty(t_pos)):
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


#def is_empty(tup):
#    '''input: a tuple'''
#    print(tup)
#    return tup[0] == tup[1]


