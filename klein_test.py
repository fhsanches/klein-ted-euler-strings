#!/usr/bin/env python3

# author: Fernando H. Sanches

from klein import Node, Euler_String, Klein, build_tree_from_dict, Indexer
import unittest
# import random

# def create_random_tree(size=1000, seed=0):
#     tree_size = 0
#     children = []

#     for node in 0..size: # for every node to be created
#         for candidate in 0..node: # for every parent candidate
#             pass

#     random.seed(seed)


def create_tree():

    #   a
    #  / \
    # b   c
    # |
    # d
    # |
    # e

    # bdeEDBcC
    # 01234567

    nodes = {
        'a': ['b', 'c'],
        'b': ['d'],
        'd': ['e'],
    }

    a = build_tree_from_dict(nodes, 'a')

    # print()
    # a.print_tree()

    return a


def create_tree_b():

    #   a
    #  / \
    # b   c
    # |  / \
    # d f   g
    # | |  / \
    # e h i   j
    #         |
    #         k

    # bdeEDBcfhHFgiIjkKJGC
    # 01234567890123456780

    a = build_tree_from_dict({
        'a': ['b', 'c'],
        'b': ['d'],
        'd': ['e'],
        'c': ['f', 'g'],
        'f': ['h'],
        'g': ['i', 'j'],
        'j': ['k'],
    }, 'a')

    return a


# z = {'a': ['b'], 3: [0], None: [4, 5, 6]}


def create_tree_c():

    #      a
    #    /   \
    #   b     c
    #  / \   / \
    # d   e f   g
    # |        / \
    # h       i   j
    #             |
    #             k

    # bdhHDeEB

    a = build_tree_from_dict({
        'a': ['b', 'c'],
        'b': ['d', 'e'],
        'd': ['h'],
        'c': ['f', 'g'],
        'g': ['i', 'j'],
        'j': ['k']
    }, 'a')

    return a


def create_tree_d():
    # modified version of c:
    # moved h (8) from d (4) to k (11) and deleted e (5) and f (6)

    #     a
    #    / \
    #   b   c
    #  /     \
    # d       g
    #        / \
    #       i   j
    #           |
    #           k
    #           |
    #           h

    # bdhHDeEB

    a = build_tree_from_dict({
        'a': ['b', 'c'],
        'b': ['d'],
        'd': [],
        'c': ['g'],
        'g': ['i', 'j'],
        'j': ['k'],
        'k': ['h']
    }, 'a')

    return a


def create_tree_e():
    # modified version of d:
    # replaced b (2) with l (12)

    # compared with c:
    # matched b with l
    # removed h
    # removed e
    # removed f
    # added h

    #     a
    #    / \
    #   l   c
    #  /     \
    # d       g
    #        / \
    #       i   j
    #           |
    #           k
    #           |
    #           h

    # bdhHDeEB

    a = build_tree_from_dict({
        'a': ['l', 'c'],
        'l': ['d'],
        'c': ['g'],
        'g': ['i', 'j'],
        'j': ['k'],
        'k': ['h']
    }, 'a')

    return a


def create_tree_singleton():

    i = 0
    label = 'ARTROOT'
    a = Node(i, label)
    i = Indexer()
    i.i_to_label = {i: label}
    i.label_to_i = {label: i}
    a.indexer = i
    a.post_processing()
    return a


class TestSuite(unittest.TestCase):

    def test_arc(self):
        tree = create_tree()

        if(len(tree.arcs) == 0):
            return

        a = tree.arcs[0]

        self.assertEqual(a.mate.mate, a)
        self.assertEqual(a.s, a.mate.t)
        self.assertEqual(a.t, a.mate.s)
        self.assertEqual(a.mate, a.mate.mate.mate)

    def test_arc_dict(self):
        a = create_tree()
        self.assertEqual(len(a.arcs_dict), 10)
        b = create_tree_b()
        self.assertEqual(len(b.arcs_dict), 22)
        c = create_tree_b()
        self.assertEqual(len(c.arcs_dict), 22)

    def test_euler(self):
        a = create_tree()

        self.assertEqual(a.E().string, [1, 2, 4, 5, -5, -4, -2, 3, -3, -1])

    def test_has_mate(self):
        a = Euler_String([1, -1, 2, -2, -3, 3, -4, 5])
        a_pos = a.get_pos()

        # print(a.arcs)

        self.assertTrue(a.has_mate(1, a_pos))
        self.assertTrue(a.has_mate(-1, a_pos))
        self.assertTrue(a.has_mate(3, a_pos))
        self.assertTrue(a.has_mate(4, a_pos))
        self.assertFalse(a.has_mate(-4, a_pos))
        self.assertFalse(a.has_mate(5, a_pos))
        self.assertFalse(a.has_mate(6, a_pos))

    def test_weights(self):
        a = create_tree()
        self.assertEqual(a.weigth, 6)
        self.assertEqual(a.children[0].children[0].weigth, 3)
        self.assertEqual(a.children[0].children[1].weigth, 1)

    def test_heavy_path(self):
        a = create_tree()
        expected = ["ARTROOT", "a", "b", "d", "e"]
        output_ls = a.heavy_path()
        output = list(map(lambda x: x.label, output_ls))
        self.assertEqual(output, expected)

    def test_difference_sequence(self):
        # a:
        #   a
        #  / \
        # b   c
        # |
        # d
        # |
        # e

        a = create_tree()
        expected = [1, -1, -3, 3, 2, -2, 4, -4, 5, -5]
        # diff_seq_2.0 = [1, -4, 4, 3, -3, 5, -5, 6, -6, -1]
        b = a.children[0].children[1]
        self.assertEqual(a.difference_sequence(a.E()), expected)
        self.assertEqual(b.difference_sequence(a.E()), [])

    def test_dict_constructors(self):
        a = Node(1, 'a')
        b = Node(2, 'b')
        self.assertEqual(a.arcs_dict, b.arcs_dict)

    def test_special_subtrees(self):

        # a:
        #   ARTROOT
        #   |
        #   a
        #  / \
        # b   c
        # |
        # d
        # |
        # e

        #     c

        a = create_tree()
        expected = ['ARTROOT', 'c']
        result = list(map(lambda x: x.label, a.special_subtrees()))
        self.assertEqual(result, expected)

        # b:
        #   ARTROOT
        #   |
        #   a
        #  / \
        # b   c
        # |  / \
        # d f   g
        # | |  / \
        # e h i   j
        #         |
        #         k

        # b
        # |
        # d f
        # | |
        # e h i
        #
        #

        b = create_tree_b()
        expected = ['ARTROOT', 'b', 'f', 'i']
        result = b.special_subtrees()
        result = list(map(lambda x: x.label, result))
        result.sort()
        self.assertEqual(result, expected)

        # c:
        #     a
        #    /  \
        #   b    c
        #  / \  / \
        # d   ef   g
        # |       / \
        # h      i   j
        #            |
        #            k

        # c':
        #
        #
        #   b
        #  / \
        # d   e f
        # |
        # h      i

        # c'': e

        # [bdhHDeEBcfFgiIjkKJGC]
        # [01234567890123456780]
        c = create_tree_c()
        expected = ['ARTROOT', 'b', 'e', 'f', 'i']
        result = c.special_subtrees()
        result = list(map(lambda x: x.label, result))
        result.sort()
        self.assertEqual(result, expected)

    # FIXME elaborate new tests
    def test_get_subtree_indexes(self):
        a = create_tree()
        b = create_tree_b()
        c = create_tree_c()

        self.assertEqual(
            a.children[0].get_subtree_indexes(),
            (1, 9))
        self.assertEqual(
            b.children[0].children[1].get_subtree_indexes(),
            (8, 20))
        self.assertEqual(
            c.children[0].children[1].children[1].get_subtree_indexes(),  # g
            (13, 19))

    def test_special_subtrees_diff_dict(self):

        #   a
        #  / \
        # b   c
        # |
        # d
        # |
        # e

        # a:
        # bdeEDBcC
        # 01234567

        # b:
        # bdeEDBcfhHFgiIjkKJGC
        # 01234567890123456780

        a = create_tree()
        b = create_tree_b()
        c = create_tree_c()

        cases = [a, b, c]
        # cases = [a]

        # cases = [b]

        for tree in cases:
            for subtree in tree.special_subtrees():
                pair = tree.get_subtree_indexes()
                self.assertIn(pair, tree.E().diff_dict)

    def test_multiple_difference_sequences(self):
        c = create_tree_c()
        c.special_subtrees()

    def test_string_removal(self):
        a = Euler_String([1, 2, 3, 4])
        a_pos = a.get_pos()
        b = Euler_String([1])
        b_pos = b.get_pos()

        (res1s, res1e) = a.remove(a_pos, 1)
        (res1sb, res1eb) = a.remove(a_pos, 4)
        (res2s, res2e) = a.remove((res1s, res1e), 4)
        res_b = b.remove(b_pos, 1)

        self.assertEqual(a[res1s:res1e], [2, 3, 4])
        self.assertEqual(a[res1sb:res1eb], [1, 2, 3])
        self.assertEqual(a[res2s:res2e], [2, 3])
        self.assertTrue(b.is_empty(res_b))
        self.assertRaises(Exception, a.remove, 3)

    def test_is_empty(self):
        a = Euler_String([])
        a_str = a.get_pos()
        b = Euler_String([1])
        b_str = b.get_pos()
        c_str = b.remove(b_str, 1)

        self.assertTrue(a.is_empty(a_str))
        self.assertFalse(b.is_empty(b_str))
        self.assertTrue(b.is_empty(c_str))

    def test_split_first(self):
        a = Euler_String([2, 3, 4, 1, -4, -3, -2, -1])

        expected_e = (2, -2)
        expected_tp_tpp = ((1, 6), (7, 8))

        (e, tp, em, tpp) = a.split_first(a.get_pos())

        self.assertEqual((e, em), expected_e)
        self.assertEqual((tp, tpp), expected_tp_tpp)

        ap_pos = (0, 7)

        expected_e = (2, -2)
        expected_tp_tpp = (1, 6), (7, 7)

        (e, tp, em, tpp) = a.split_first(ap_pos)
        self.assertEqual((e, em), expected_e)
        self.assertEqual((tp, tpp), expected_tp_tpp)

    def test_split_last(self):
        a = Euler_String([2, 3, 4, 1, -4, -3, -2, -1])

        expected_e = (-1, 1)
        expected_tp_tpp = ((0, 3), (4, 7))

        (tp, em, tpp, e) = a.split_last(a.get_pos())

        self.assertEqual((e, em), expected_e)
        self.assertEqual((tp, tpp), expected_tp_tpp)

        ap_pos = (2, 8)

        expected_e = (-1, 1)
        expected_tp_tpp = ((2, 3), (4, 7))

        (tp, em, tpp, e) = a.split_last(ap_pos)

        self.assertEqual((e, em), expected_e)
        self.assertEqual((tp, tpp), expected_tp_tpp)

    def test_diff_dict(self):
        a = create_tree()
        a_s = a.E()
        # abdeEDBcCA
        # bdeEDBcCA
        # bdeEDBcC
        # bdeEDBc
        # bdeEDB
        # deEDB
        # deED
        # eED
        # eE
        # E
        # ""
        print('diff')
        print(a_s.diff_dict)

        # a = [1, -1, 2, 4, 5, -5, -4, -2, 3, -3], -3
        self.assertEqual(a_s.diff_dict[(0, 10)],  0)
        # a = [-1, 2, 4, 5, -5, -4, -2, 3, -3], -3
        self.assertEqual(a_s.diff_dict[(1, 10)],  1)
        # a = [2, 4, 5, -5, -4, -2, 3, -3], -3
        self.assertEqual(a_s.diff_dict[(1, 9)],  1)
        # a = [2, 4, 5, -5, -4, -2, 3], 3
        self.assertEqual(a_s.diff_dict[(1, 8)],  1)
        # a = [2, 4, 5, -5, -4, -2] 2
        self.assertEqual(a_s.diff_dict[(1, 7)],  0)
        # a = [4, 5, -5, -4, -2] -2
        self.assertEqual(a_s.diff_dict[(2, 7)],  1)
        # a = [4, 5, -5, -4] 4
        self.assertEqual(a_s.diff_dict[(2, 6)],  0)
        # a = [5, -5, -4] -4
        self.assertEqual(a_s.diff_dict[(3, 6)],  1)
        # a = [5, -5] 5
        self.assertEqual(a_s.diff_dict[(3, 5)],  0)
        # a = [-5] -5
        # self.assertEqual(a_s.diff_dict[(3, 4)],  1)

    # FIXME re-elaborate tests
    def test_next_string(self):
        a = create_tree()
        at = a.E()
        # a = [1, 2, 4, 5, -5, -4, -2, 3, -3, -1]
        # # diff seq = [1, -1, -3, 3, 2, -2, 3, -3, 4, -4]
        pos = at.get_pos()

        print(at)
        self.assertEqual(at.next_string(pos), ((1, 10), 1))
        self.assertEqual(at.next_string((1, 10)), ((1, 9), -1))
        # self.assertEqual(at.next_string((1, 9)), ((1, 8), -2))

    def test_delete_from_s(self):

        at = create_tree()
        a = at.children[0].E()
        bt = create_tree_b()
        b = bt.children[0].E()
        ct = create_tree_c()
        c = ct.children[0].E()
        ot = create_tree_singleton()
        one = ot.E()

        one_pos = one.get_pos()
        a_pos = a.get_pos()
        b_pos = b.get_pos()
        c_pos = c.get_pos()

        k1 = Klein(ot, ot)
        self.assertEqual(
            k1.delete_from_s((0, 0), (0, 0)),
            float('inf'))
        k2 = Klein(at, ot)
        self.assertEqual(
            k2.delete_from_s(a_pos, one_pos),
            at.weigth - 1)
        k3 = Klein(bt, ot)
        self.assertEqual(
            k3.delete_from_s(b_pos, one_pos),
            bt.weigth - 1)
        k4 = Klein(ct, ot)
        self.assertEqual(
            k4.delete_from_s(c_pos, one_pos),
            ct.weigth - 1)

    def test_delete_from_t(self):

        at = create_tree()
        a = at.E()
        bt = create_tree_b()
        b = bt.E()
        ct = create_tree_c()
        c = ct.E()
        ot = create_tree_singleton()
        one = ot.E()

        one_pos = one.get_pos()
        print("op: " + str(one_pos))
        # one_pos = (0, 1)

        a_pos = a.get_pos()
        b_pos = b.get_pos()
        c_pos = c.get_pos()

        k1 = Klein(ot, ot)
        self.assertEqual(
            k1.delete_from_t((0, 0), (0, 0)),
            float('inf'))
        k2 = Klein(ot, at)
        self.assertEqual(
            k2.delete_from_t(one_pos, a_pos),
            at.weigth - 1)  # -1 to discount the artificial root
        k3 = Klein(ot, bt)
        self.assertEqual(
            k3.delete_from_t(one_pos, b_pos),
            bt.weigth - 1)
        k4 = Klein(ot, ct)
        self.assertEqual(
            k4.delete_from_t(one_pos, c_pos),
            ct.weigth - 1)

    def test_match(self):

        at = create_tree()
        a = at.E()
        bt = create_tree_b()
        b = bt.E()
        ct = create_tree_c()
        c = ct.E()
        dt = create_tree_d()
        d = dt.E()
        et = create_tree_e()
        e = et.E()

        ot = create_tree_singleton()
        one = ot.E()

        a_pos = a.get_pos()
        b_pos = b.get_pos()
        c_pos = c.get_pos()
        d_pos = d.get_pos()
        e_pos = e.get_pos()
        one_pos = one.get_pos()

        k1 = Klein(ot, ot)
        self.assertEqual(k1.match(one_pos, one_pos), 0)

        k2 = Klein(at, at)
        self.assertEqual(k2.match(a_pos, a_pos), 0)

        k3 = Klein(bt, bt)
        self.assertEqual(k3.match(b_pos, b_pos), 0)

        k4 = Klein(at, bt)
        self.assertGreater(k4.match(a_pos, b_pos), 0)

        k5 = Klein(bt, ct)
        self.assertGreater(k5.match(b_pos, c_pos), 0)

        k6 = Klein(ct, dt)
        self.assertEqual(k6.match(c_pos, d_pos), 4)

        k7 = Klein(dt, et)
        self.assertEqual(k7.match(d_pos, e_pos), 1)

        k7 = Klein(ct, et)
        self.assertEqual(k7.match(c_pos, e_pos), 5)


#   a
#  / \
# b   c
# |
# d
# |
# e

# bdeEDBcC
# 01234567

if(__name__ == '__main__'):
    unittest.main()
