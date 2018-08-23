#!/usr/bin/env python3

from klein import Node, Euler_String, Klein
import unittest


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

    a = Node(1)
    b = Node(2, a)
    c = Node(3, a)
    d = Node(4, a)
    e = Node(5, a)

    a.add_child(b)
    a.add_child(c)
    b.add_child(d)
    d.add_child(e)

    a.post_processing(a)

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

    a = Node(1)
    b = Node(2, a)
    c = Node(3, a)
    d = Node(4, a)
    e = Node(5, a)
    f = Node(6, a)
    g = Node(7, a)
    h = Node(8, a)
    i = Node(9, a)
    j = Node(10, a)
    k = Node(11, a)
    a.add_child(b)

    a.add_child(c)
    b.add_child(d)
    d.add_child(e)
    c.add_child(f)
    c.add_child(g)
    f.add_child(h)
    g.add_child(i)
    g.add_child(j)
    j.add_child(k)

    a.post_processing(a)

    return a


def create_tree_c():

    #     a
    #    /  \
    #   b    c
    #  / \  / \
    # d   ef   g
    # |       / \
    # h      i   j
    #            |
    #            k

    #bdhHDeEB

    a = Node(1)
    b = Node(2, a)
    c = Node(3, a)
    d = Node(4, a)
    e = Node(5, a)
    f = Node(6, a)
    g = Node(7, a)
    h = Node(8, a)
    i = Node(9, a)
    j = Node(10, a)
    k = Node(11, a)

    a.add_child(b)
    a.add_child(c)
    b.add_child(d)
    b.add_child(e)
    d.add_child(h)
    c.add_child(f)
    c.add_child(g)
    g.add_child(i)
    g.add_child(j)
    j.add_child(k)

    a.post_processing(a)

    return a


def create_tree_singleton():
        a = Node(1)
        a.post_processing(a)
        return a


class TestSuite(unittest.TestCase):

    k = Klein()

    def test_list_split(self):
        ls = [1, 2, 3, 4]
        self.assertEqual(list_split(ls, 3), [[1, 2], [4]])
        self.assertEqual(list_split(ls, 2), [[1], [3, 4]])

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
        self.assertEqual(len(a.arcs_dict), 8)
        b = create_tree_b()
        self.assertEqual(len(b.arcs_dict), 20)
        c = create_tree_b()
        self.assertEqual(len(c.arcs_dict), 20)

    def test_euler(self):
        a = create_tree()

        self.assertEqual(a.E().string, [2, 4, 5, -5, -4, -2, 3, -3])
        #self.assertEqual(a.children[0].E().string, [4, 5, -5, -4])
        #self.assertEqual(a.children[1].E().string, [])

    def test_has_mate(self):
        a = Euler_String([1, -1, 2, -2, -3, 3, -4, 5])
        a_pos = a.get_pos()

        self.assertTrue(a.has_mate(1, a_pos))
        self.assertTrue(a.has_mate(-1, a_pos))
        self.assertTrue(a.has_mate(3, a_pos))
        self.assertTrue(a.has_mate(4, a_pos))
        self.assertFalse(a.has_mate(-4, a_pos))
        self.assertFalse(a.has_mate(5, a_pos))
        self.assertFalse(a.has_mate(6, a_pos))

    def test_weights(self):
        a = create_tree()
        self.assertEqual(a.weigth, 5)
        self.assertEqual(a.children[0].weigth, 3)
        self.assertEqual(a.children[1].weigth, 1)

    def test_heavy_path(self):
        a = create_tree()
        # expected = ["a", "b", "d", "e"]
        expected = [1, 2, 4, 5]
        output_ls = a.heavy_path()
        output = map(lambda x: x.label, output_ls)
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
        expected = [2, -3, 3, -2, 4, -4, 5, -5]
        b = a.children[1]
        self.assertEqual(a.difference_sequence(a.E()), expected)
        self.assertEqual(b.difference_sequence(a.E()), [])

    def test_dict_constructors(self):
        a = Node(1)
        b = Node(2, a)
        self.assertEqual(a.arcs_dict, b.arcs_dict)

    def test_special_subtrees(self):

        # a:
        #   a
        #  / \
        # b   c
        # |
        # d
        # |
        # e

        #     c

        a = create_tree()
        expected = [3]
        result = map(lambda x: x.label, a.special_subtrees())
        self.assertEqual(result, expected)

        # b:
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
        expected = [2, 6, 9]
        result = b.special_subtrees()
        result = map(lambda x: x.label, result)
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
        expected = [2, 5, 6, 9]
        result = c.special_subtrees()
        result = map(lambda x: x.label, result)
        result.sort()
        self.assertEqual(result, expected)

    def test_get_subtree_indexes(self):

        a = create_tree()
        b = create_tree_b()
        c = create_tree_c()

        print("label:::")
        print(a.children[0].label)

        self.assertEqual(a.children[0].get_subtree_indexes(), (1, 5))
        self.assertEqual(b.children[1].get_subtree_indexes(), (7, 19))
        self.assertEqual(c.children[1].children[1].get_subtree_indexes(),  # g
                         (12, 18))

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

        # cases = [a, b, c]
        #cases = [a]

        cases = [b]

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
        expected_tp_tpp_str = ([3, 4, 1, -4, -3], [-1])

        (e, (st1, ed1), em, (st2, ed2)) = a.split_first(2, True)

        str1 = a[st1:ed1]
        str2 = a[st2:ed2]

        self.assertEqual((e, em), expected_e)
        self.assertEqual((str1, str2), expected_tp_tpp_str)

    def test_split_last(self):
        a = Euler_String([2, 3, 4, 1, -4, -3, -2, -1])

        expected_e = (-1, 1)
        expected_res_str = ([2, 3, 4], [-4, -3, -2])

        ((st1, ed1), em, (st2, ed2), e) = a.split_last(-1, True)
        ls1 = a[st1:ed1]
        ls2 = a[st2:ed2]

        self.assertEqual((e, em), expected_e)
        self.assertEqual((ls1, ls2), expected_res_str)

    def test_diff_dict(self):
        a = create_tree()
        a_s = a.E()
        # a = [2, 4, 5, -5, -4, -2, 3, -3]
        # diff seq = [2, -3, 3, -2, 4, -4, 5, -5]

        # a = [2, 4, 5, -5, -4, -2, 3, -3], 2
        self.assertEqual(a_s.diff_dict[(0, 8)],  0)
        # a = [4, 5, -5, -4, -2, 3, -3], -3
        self.assertEqual(a_s.diff_dict[(1, 8)],  1)
        # a = [4, 5, -5, -4, -2, 3], 3
        self.assertEqual(a_s.diff_dict[(1, 7)],  1)
        # a = [4, 5, -5, -4, -2], -2
        self.assertEqual(a_s.diff_dict[(1, 6)],  1)
        # a = [4, 5, -5, -4], 4
        self.assertEqual(a_s.diff_dict[(1, 5)],  0)
        # a = [5, -5, -4], -4
        self.assertEqual(a_s.diff_dict[(2, 5)],  1)
        # a = [5, -5], 5
        self.assertEqual(a_s.diff_dict[(2, 4)],  0)
        # a = [-5], -5
        self.assertEqual(a_s.diff_dict[(3, 4)],  0)

    def test_next_string(self):
        a = create_tree()
        at = a.E()
        # a = [2, 4, 5, -5, -4, -2, 3, -3]
        # diff seq = [2, -3, 3, -2, 4, -4, 5, -5]
        pos = at.get_pos()

        self.assertEqual(at.next_string(pos), ((1, 8), 2))
        self.assertEqual(at.next_string((1, 8)), ((1, 7), -3))
        self.assertEqual(at.next_string((1, 7)), ((1, 6), 3))

    def test_remove_from_s(self):
        k = Klein()

        at = create_tree()
        a = at.E()
        bt = create_tree_b()
        b = bt.E()
        ct = create_tree_c()
        c = ct.E()
        ot = create_tree_singleton()
        one = ot.E()

        one_pos = one.get_pos()
        a_pos = a.get_pos()
        b_pos = b.get_pos()
        c_pos = c.get_pos()

        self.assertEqual(k.delete_from_s(one, one_pos, one, one_pos),
                         float('inf'))
        self.assertEqual(k.delete_from_s(a, a_pos, one, one_pos), 4)
        self.assertEqual(k.delete_from_s(b, b_pos, one, one_pos), 10)
        self.assertEqual(k.delete_from_s(c, c_pos, one, one_pos), 10)

    def test_remove_from_t(self):
        k = Klein()

        at = create_tree()
        a = at.E()
        bt = create_tree_b()
        b = bt.E()
        ct = create_tree_c()
        c = ct.E()
        ot = create_tree_singleton()
        one = ot.E()

        one_pos = one.get_pos()
        a_pos = a.get_pos()
        b_pos = b.get_pos()
        c_pos = c.get_pos()

        self.assertEqual(k.delete_from_t(one, one_pos, one, one_pos),
                         float('inf'))
        self.assertEqual(k.delete_from_t(one, one_pos, a, a_pos), 4)
        self.assertEqual(k.delete_from_t(one, one_pos, b, b_pos), 10)
        self.assertEqual(k.delete_from_t(one, one_pos, c, c_pos), 10)

    def test_match(self):
        k = Klein()

        at = create_tree()
        a = at.E()
        bt = create_tree_b()
        b = bt.E()
        ct = create_tree_c()
        c = ct.E()
        ot = create_tree_singleton()
        one = ot.E()

        a_pos = a.get_pos()
        b_pos = b.get_pos()
        c_pos = c.get_pos()
        one_pos = one.get_pos()

        self.assertEqual(k.match(one, one_pos, one, one_pos), 0)
        # self.assertEqual(k.match(a, a_pos, a, a_pos), 0)
        # self.assertEqual(k.match(b, b_pos, b, b_pos), 0)
        # self.assertGreater(k.match(a, a_pos, b, b_pos), 0)
        self.assertGreater(k.match(b, b_pos, c, c_pos), 0)


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
