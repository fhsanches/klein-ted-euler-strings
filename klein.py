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
        return ls


class Node:
    def __init__(self, label, has_root=None):
        self.children = []
        self.arcs = []
        self.label = label
        self.weigth = 1
        self.euler = None
        self.root = has_root

        if(not has_root):
            self.arcs_dict = {}
        else:
            self.arcs_dict = self.root.arcs_dict

    def __iter__(self):
        for v in chain(*imap(iter, self.children)):
            yield v
        yield self

    def euler_list_compute(self):
        res = []
        for arc in self.arcs:
            res.append(arc.label)
            res.extend(arc.t.euler_list_compute())
            res.append(arc.mate.label)
        # self.euler = res
        return res

    def E(self):
        if(not self.euler):
            if(self.root):  # I have a root
                self.euler = self.root.E()
            else:  # I AM the root
                el = self.euler_list_compute()
                self.euler = Euler_String(el)
            return self.euler
        else:
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
        # self.set_roots(self)
        self.E()  # calculate euler strings
        self.proccess_special_subtrees()

    def proccess_special_subtrees(self):
        # main tree
        E = self.E()
        diff_seq = self.difference_sequence(E)
        pos = E.get_pos()
        self.calculate_special_substrings(diff_seq, pos)

        # other special subtrees
        for tree in self.special_subtrees():
            pos = tree.get_subtree_indexes()
            path = tree.heavy_path()
            diff_seq = tree.difference_sequence(E, pos, path)
            self.calculate_special_substrings(diff_seq, pos)

            # if(tree.weigth > 1):
            #     print("special!" + str(tree.label))
            #     pos = tree.get_surounding_arcs_indexes()
            #     print(pos)
            #     path = tree.heavy_path()
            #     diff_seq = tree.difference_sequence(E, pos, path)
            #     self.set_diff_dict(diff_seq, pos)
            # else:
            #     print("empty subtree at " + str(tree.label))

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

    def difference_sequence(self, E, pos=None, path=None, path_pos=1):
        if(not self.children):  # is empty
            return []
        else:
            if(not path):
                path = self.heavy_path()

            if(not pos):
                (st, ed) = (0, len(E.string))
            else:
                (st, ed) = pos

            v = path[path_pos]  # self's child in P

            p = self.arcs_dict[(self.label, v.label)]
            q = p.mate

            rv = E.arcs[p.label]
            vr = E.arcs[q.label]

            T_left = E[st:rv+1]  # ending with p
            T_right = E[vr:ed]  # starting with p

            res = T_left + T_right[::-1] + v.difference_sequence(E,
                                                                 (rv+1, vr),
                                                                 path,
                                                                 path_pos+1)

            self.difference_seq = res

            return res

    def calculate_special_substrings(self, difference_sequence, pos):
        '''
        builds a direction dict and sets it in the euler string object
        diff[(i,j)] is "0" if the deletion of E at (i,j) is to the left,
        "1" otherwise
        reminder: (i,j) follows slice notation e[i:j], i.e., j is not included
        '''
        euler = self.E()

        if(not(euler.diff_dict)):
            diff = {}
        else:
            diff = euler.diff_dict

        (i, j) = pos

        # if(not difference_sequence):  # leaf node, empty difference sequence
        # diff[(i, j)] = i
        #   diff[(i+1, j)] = i+1

        for label in difference_sequence:
            if(label == euler[i]):
                diff[(i, j)] = 0
                i += 1
            elif(label == euler[j-1]):
                diff[(i, j)] = 1
                j -= 1
            else:
                raise Exception("Bad difference sequence")

            euler.diff_dict = diff

    def special_subtrees(self):
        hpath = self.heavy_path()
        ls = []
        for node in hpath:
            for child in node.children:
                if(child not in hpath):
                    ls.append(child)
                    ls.extend(child.special_subtrees())

        return ls

    def get_subtree_indexes(self):
        E = self.E()
        if(not self.children):
            return (0, 0)
        else:
            p = self.arcs[0].label
            q = self.arcs[-1].mate.label

            i = E.arcs[p]
            j = E.arcs[q]

            return(i, j+1)

    # def get_surounding_arcs_indexes(self):
    #     p = self.arcs[0].label
    #     q = self.arcs[0].mate.label

    #     i = self.E().arcs[p]
    #     j = self.E().arcs[q]

    #     if(self.weigth > 1):
    #         # print("got indexes for:")
    #         # print(i, j)
    #         return(i, j)
    #     else:
    #         print("This MAY be a bit dangerous")
    #         return (0, 0)


class Euler_String():
    '''
    Encapsulates a string and its difference sequence. \
    Overrides access methods to the string
    '''
    def __init__(self, string):
        self.string = string  # list of labels

        self.arcs = [None] * (len(string)*2+2)  # fixme esse *2 e' gambiarra

        for (index, label) in enumerate(self.string):
            # print("?error with " + str(label))
            self.arcs[label] = index

        self.start = 0
        self.end = len(string)

        self.diff_dict = {}
        self.diff_seq = None

    def get_pos(self):
        return(self.start, self.end)

    def __str__(self):
        return "<str: " + str(self.string) + ">"

    def __getitem__(self, index):
        return self.string[index]

    def next_string(self, pos):
        '''
        returns a pair (new_pos, symbol), where newpos represents pos - symbol
        abuses the fact that the diff dict uses 0 and 1 choose symbol correctly
        '''
        (st, ed) = pos
        # print(self.diff_dict)
        direction = self.diff_dict[pos]
        if(direction == 0):
            new_pos = (st+1, ed)
            symbol = self.string[st]
        else:
            new_pos = (st, ed-1)
            symbol = self.string[ed-1]
        return (new_pos, symbol)

    def difference_symbol(self, pos):
        return self.next_string(pos)[1]

    def has_mate(self, symbol, pos):
        (st, ed) = pos
        mate = find_mate(symbol)
        x = self.arcs[mate]
        if(x >= st and x < ed):
            return True
        else:
            return False

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

    # def build_diff_dict(self, pos):
    #     if(not self.diff_seq):
    #         self.difference_sequence()

    #     i = self.start
    #     j = self.end - 1

    #     for element in self.difference_seq:
    #         element_pos = self.arcs[element]
    #         if(element_pos == i):
    #             self.diff_dict[(i, j)] = True
    #         elif(element_pos == j):
    #             self.diff_dict[(i, j)] = False
    #         else:
    #             raise Exception("Bad difference sequence")

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

        (next_t, e) = t.next_string(t_pos)

        if(t.has_mate(e, next_t)):
            return(self.dist(s, s_pos, t, next_t) + self.cdel(e, t))
        else:
            return(self.dist(s, s_pos, t, next_t))

    def delete_from_s(self, s, s_pos, t, t_pos):
        (s_st, s_ed) = s_pos
        (t_st, t_ed) = t_pos

        if(s.is_empty(s_pos)):
            return INFTY
        elif(t.is_empty(t_pos)):
            e = s[s_ed-1]
            new_s = (s_st, s_ed-1)
        else:
            (next_t, symbol) = t.next_string(t_pos)
            if(symbol == t[t_ed-1]):
                e = s[s_ed-1]
                new_s = (s_st, s_ed-1)
            else:
                e = s[s_st]
                new_s = (s_st+1, s_ed)
        if(s.has_mate(e, s_pos)):
            return self.dist(s, new_s, t, t_pos) + self.cdel(e, s)
        else:
            return self.dist(s, new_s, t, t_pos)

    def match(self, s, s_pos, t, t_pos):
        if(s.is_empty(s_pos) and t.is_empty(t_pos)):
            return 0
        if(s.is_empty(s_pos) or t.is_empty(t_pos)):
            return INFTY
        e = t.difference_symbol(t_pos)
        if(e == t[0]):
            e_p = s[0]
        else:
            e_p = s[-1]
        if((not t.has_mate(e, t_pos)) or (not s.has_mate(e_p, s_pos))):
            return INFTY
        if(e == t[0]):
            (e, tpp, em, tp) = t.split_first(e)
            (ep, spp, epm, sp) = s.split_first(e, True)
        else:
            (tp, em, tpp, e) = t.split_last(e)
            (sp, epm, spp, ep) = s.split_last(e, True)
        return \
            self.dist(s, sp, t, tp) + \
            self.dist(s, spp, t, tpp) + \
            self.cmatch(e, ep)

    def dist(self, s, s_pos, t, t_pos):
        return min(self.delete_from_s(s, s_pos, t, t_pos),
                   self.delete_from_t(s, s_pos, t, t_pos),
                   self.match(s, s_pos, t, t_pos))

    def cdel(self, symbol, string):
        return 1

    def cmatch(self, symbol1, symbol2):
        if(symbol1 == symbol2):
            return 0
        return 1


def find_mate(c):
    return c * -1


def list_split(ls, x):
        i = ls.index(x)
        return [ls[0:i], ls[i+1:]]

# def is_empty(tup):
#     '''input: a tuple'''
#     print(tup)
#     return tup[0] == tup[1]
