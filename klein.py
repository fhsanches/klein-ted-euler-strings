#!/usr/bin/env python3
import functools

INFTY = float('inf')


def memoize(func):
    cache = func.cache = {}

    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return memoized_func


class Arc:
    def __init__(self, s, t, value=None, mate=None):  # source, target
        '''
        initializes arc, creates mate (if not given), add self to "arcs" dict
        '''
        self.s = s
        self.t = t
        self.value = value
        if(mate is None):
            self.mate = self.create_mate()
        else:
            self.mate = mate
        s.arcs_dict[(s.label, t.label)] = self

    def create_mate(self):
        mate_value = find_mate(self.value)
        mate = Arc(self.t, self.s, mate_value, self)
        return mate

    def euler_visit(self):
        ls = [self.label]
        ls.extend(self.t.euler_visit())
        ls.append(self.mate.label)
        return ls


class Node:
    def __init__(self, value, label, has_root=None):
        self.children = []
        self.arcs = []
        self.value = value
        self.label = label
        self.weigth = 1
        self.euler = None
        self.root = has_root

        if(not has_root):
            self.arcs_dict = {}
        else:
            self.arcs_dict = self.root.arcs_dict

    def print_tree(self):
        if self.children:
            self.children[0].print_tree()
        for child in self.children[1:]:
            child.print_tree()

    def euler_list_compute(self):
        res = []
        for arc in self.arcs:
            res.append(arc.value)
            res.extend(arc.t.euler_list_compute())
            res.append(arc.mate.value)
        return res

    def E(self):
        if(not self.euler):
            if(self.root):  # I have a root
                self.euler = self.root.E()
            else:  # I AM the root
                el = self.euler_list_compute()
                self.euler = Euler_String(el)
            self.euler.string = self.euler.string
            return self.euler
        else:
            self.euler.string = self.euler.string
            return self.euler

    def add_child(self, child):
        self.children.append(child)
        arc = Arc(self, child, child.value)
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

    def difference_sequence(self, E, pos=None, path=None, path_pos=0):
        '''
        E = euler string
        pos = pair with position
        path = path for which it is being calculated (default heavy)
        path pos = index in path of the root being
        '''
        if(not self.children):  # is empty
            return []
        else:
            if(not path):
                path = self.heavy_path()

            if(not pos):
                (st, ed) = (E.start, E.end)
            else:
                (st, ed) = pos

            v = path[path_pos+1]  # self's child in P

            p = self.arcs_dict[(self.label, v.label)]
            q = p.mate

            rv = E.arcs[p.value]
            vr = E.arcs[q.value]

            T_left = E[st:rv]  # ending with p
            T_right = E[vr+1:ed]  # starting with p

            res = T_left + \
                T_right[::-1] + \
                [E[rv], E[vr]] + \
                v.difference_sequence(E,
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

        difference_sequence = difference_sequence

        for label in difference_sequence:
            if(label == euler[i]):
                diff[(i, j)] = 0
                i += 1
            elif(label == euler[j-1]):
                diff[(i, j)] = 1
                j -= 1
            else:
                raise Exception("Bad difference sequence "
                                + str(label)
                                + " vs "
                                + str(euler[i])
                                + ","
                                + str(euler[j-1])
                                + " in \n" + str(difference_sequence)
                                + " for \n" + str(euler))

            euler.diff_dict = diff

    def special_subtrees(self):
        hpath = self.heavy_path()
        n = len(hpath)
        ls = [self]
        for i, node in enumerate(hpath):
            for child in node.children:
                if child != hpath[(i + 1) % n]:
                    ls.extend(child.special_subtrees())

        return ls

    def get_subtree_indexes(self):
        E = self.E()
        if(not self.children):
            return (0, 0)
        else:
            p = self.arcs[0].value
            q = self.arcs[-1].mate.value

            i = E.arcs[p]
            j = E.arcs[q]

            return(i, j+1)


class Indexer():
    '''
    relates each label with an index
    1 instance per tree
    tables will be kept in memory
    '''
    def __init__(self):
        self.i = 0
        self.label_to_i = {}
        self.i_to_label = {}

    def count(self):
        '''
        acts as a counter
        '''
        self.i += 1
        return self.i

    def transform_dict(self, adj_dict):
        '''
        receives a dict in the form: {label: [label1, label...]}
        returns a dict in the form: {(0, label): [(1, label1), (2, label2)...]
        '''

        label_to_i = self.label_to_i
        i_to_label = self.i_to_label

        # label_to_i[0] = 0
        # i_to_label[0] = 0

        for (label, children_label) in adj_dict.items():
            if label not in label_to_i:
                i = self.count()
                label_to_i[label] = i
                i_to_label[i] = label
            for child_label in children_label:
                if child_label not in label_to_i:
                    i = self.count()
                    label_to_i[child_label] = i
                    i_to_label[i] = child_label

        new_dict = {}

        for label, children_label in adj_dict.items():
            new_dict[(self.label_to_i[label], label)] = \
                                      [(self.label_to_i[clabel], clabel)
                                       for clabel in children_label]

        return new_dict


def build_tree_from_dict(adj_dict, root_label=0):
    '''
    builds a tree from a dict in the format:
    {a : [b,c], c: [d,e,f], f = [g] ...}
    leaves can be ommited as keys
    the root must be in the dict
    '''

    nodes = {}

    # transform dict to use identifiers instead of labels
    i = Indexer()
    adj_dict = i.transform_dict(adj_dict)  # now in form (i, label)

    root = Node(0, root_label)
    nodes[0] = root

    # build the tree
    for (parent_val, child_values) in adj_dict.items():
        if not nodes.get(parent_val[0]):
            nodes[parent_val[0]] = Node(parent_val[0], parent_val[1])

        parent = nodes[parent_val[0]]

        for child_val in child_values:
            if not nodes.get(child_val[0]):
                nodes[child_val[0]] = Node(child_val[0], child_val[1], root)

            child = nodes[child_val[0]]

            parent.add_child(child)

    # add old root as child of new root
    root.add_child(nodes[i.label_to_i[root_label]])

    root.post_processing()
    root.indexer = i
    return root


class Euler_String():
    '''
    Encapsulates a string and its difference sequence. \
    Overrides access methods to the string
    '''
    def __init__(self, string):
        self.string = string  # list of values, eg. [1, 3, 4, -4, -3, 1, 2, -2]

        self.arcs = [None] * (len(string) + 4)

        # index arcs so I can find them in O(1)
        for (index, val) in enumerate(self.string):
            self.arcs[val] = index

        self.start = 0
        self.end = len(string)

        self.diff_dict = {}
        self.diff_seq = None

    def get_pos(self):
        return(self.start, self.end)

    def __str__(self):
        return "<str: " + str(self.string) + \
            ", st: " + str(self.start) + ", ed: " + str(self.end) + ">"

    def __getitem__(self, index):
        return self.string[index]

    def next_string(self, pos):
        '''
        Returns a pair (new_pos, symbol), where newpos represents pos - symbol.
        '''
        (st, ed) = pos
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
        if (x is not None) and (st <= x < ed):
            return True
        else:
            return False

    def index_of_mate(self, symbol):
        mate = symbol * -1
        return self.arcs[mate]

    def split_first(self, pos):
        st, ed = pos
        e = self.string[st]
        em = find_mate(e)
        mate_index = self.index_of_mate(e)

        tpp = (st+1, mate_index)
        tp = (mate_index + 1, ed)

        return(e, tpp, em, tp)

    def split_last(self, pos):
        st, ed = pos
        e = self.string[ed-1]
        em = find_mate(e)
        mate_index = self.index_of_mate(e)

        tp = (st, mate_index)
        tpp = (mate_index + 1, ed-1)

        return(tp, em, tpp, e)

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
        return (st >= ed)


class Klein():
    def __init__(self, f, g):
        self.f = f
        self.g = g
        self.s = f.E()
        self.t = g.E()
        self.tests_num = 0

        self.delta = {}

    def delete_from_t(self, s_pos, t_pos):
        t = self.t

        if(t.is_empty(t_pos)):
            return INFTY

        (next_t_pos, e) = t.next_string(t_pos)

        if(t.has_mate(e, next_t_pos)):
            return(self.dist(s_pos, next_t_pos) + self.cdel(e))
        else:
            return(self.dist(s_pos, next_t_pos))

    def delete_from_s(self, s_pos, t_pos):
        s = self.s
        t = self.t

        (s_st, s_ed) = s_pos
        (t_st, t_ed) = t_pos

        if(s.is_empty(s_pos)):
            return INFTY
        elif(t.is_empty(t_pos)):
            e = s[s_ed-1]
            next_s_pos = (s_st, s_ed-1)
        else:
            (next_t, symbol) = t.next_string(t_pos)
            if(symbol == t[t_ed-1]):
                e = s[s_ed-1]
                next_s_pos = (s_st, s_ed-1)
            else:
                e = s[s_st]
                next_s_pos = (s_st+1, s_ed)
        if(s.has_mate(e, s_pos)):
            return self.dist(next_s_pos, t_pos) + self.cdel(e)
        else:
            return self.dist(next_s_pos, t_pos)

    def match(self, s_pos, t_pos):
        s = self.s
        t = self.t

        t_st, t_ed = t_pos
        s_st, s_ed = s_pos

        if s.is_empty(s_pos) and t.is_empty(t_pos):
            return 0
        if s.is_empty(s_pos) or t.is_empty(t_pos):
            return INFTY
        e = t.difference_symbol(t_pos)

        if e == t[0]:
            ep = s[s_st]
        else:
            ep = s[s_ed - 1]
        if (not t.has_mate(e, t_pos)) or (not s.has_mate(ep, s_pos)):
            return INFTY
        if e == t[t_st]:
            e, tpp, em, tp = t.split_first(t_pos)
            ep, spp, epm, sp = s.split_first(s_pos)
        else:
            tp, em, tpp, e = t.split_last(t_pos)
            sp, epm, spp, ep = s.split_last(s_pos)
        return \
            self.dist(sp, tp) + \
            self.dist(spp, tpp) + \
            self.cmatch(ep, e)

    @memoize
    def dist(self, s_pos, t_pos):

        self.tests_num += 1

        if (s_pos, t_pos) in self.delta.keys():
            return self.delta[(s_pos, t_pos)]

        res = min(self.delete_from_s(s_pos, t_pos),
                  self.delete_from_t(s_pos, t_pos),
                  self.match(s_pos, t_pos))

        self.delta[(s_pos, t_pos)] = res
        return res

    def cdel(self, val1):
        return 1

    def cmatch(self, val1, val2):
        if val1 < 0:
            val1 *= -1
        if val2 < 0:
            val2 *= -1
        symbol1 = self.f.indexer.i_to_label[val1]
        symbol2 = self.g.indexer.i_to_label[val2]
        if(symbol1 == symbol2):
            return 0
        return 1


def i2n(lista):
    answer = ''
    for i in lista:
        answer += chr(ord('a') + i - 1) if i > 0 else chr(ord('A') - i - 1)
    return answer


def find_mate(c):
    return c * -1


def substrings(e1):
    ss = [(i, j) for i in range(e1.start, e1.end-1)
          for j in range(i+1, e1.end)]
    return ss


def rel_s(t):
    '''returns the relevant substrings of a tree'''
    pairs = t.diff_dict.keys()
    res = pairs
    res = sorted(pairs, key=lambda tup: (tup[1] - tup[0]))
    return res


def Klein_TED(dict_t1, dict_t2, dict_t1_root=0, dict_t2_root=0):
    '''returns a pair
    (x,y),
    where:
    x = the value for the TED
    y = the number of times "dist" was called (including trivial calls)
    '''

    t1 = build_tree_from_dict(dict_t1, dict_t1_root)
    t2 = build_tree_from_dict(dict_t2, dict_t2_root)
    (t1_E, t2_E) = (t1.E(), t2.E())
    k = Klein(t1, t2)

    for s in substrings(t1_E):
        for t in rel_s(t2_E):
            k.dist(s, t)

    result = (k.dist(t1_E.get_pos(), t2_E.get_pos()), k.tests_num)  # pair

    k.dist.cache.clear()

    return result
