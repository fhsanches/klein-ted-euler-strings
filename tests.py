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

    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)

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

    # def test_list_split(self):
    #     ls = [1, 2, 3, 4]
    #     self.assertEqual(list_split(ls, 3), [[1, 2], [4]])
    #     self.assertEqual(list_split(ls, 2), [[1], [3, 4]])

    def test_arc(self):
        tree = create_tree()

        if(len(tree.arcs) == 0):
            return

        a = tree.arcs[0]

        self.assertEqual(a.mate.mate, a)
        self.assertEqual(a.s, a.mate.t)
        self.assertEqual(a.t, a.mate.s)
        self.assertEqual(a.mate, a.mate.mate.mate)

    def test_euler(self):
        a = create_tree()

        self.assertEqual(a.E().string, [2, 4, 5, -5, -4, -2, 3, -3])
        self.assertEqual(a.children[0].E().string, [4, 5, -5, -4])
        self.assertEqual(a.children[1].E().string, [])

    # def test_string_index(self):
    #     euler_string_a = Euler_String([2, -3, 3, -2, 4, -4, 5, -5])
    #     self.assertEqual(a[0], 2)
    #     self.assertEqual(a[1], -3)
    #     self.assertEqual(a[-1], -5)

    #     #                            [ 0,  1, 2,  3, 4,  5, 6,  7]
    #     #                            [-8, -7,-6, -5,-4, -3,-2, -1]
    #     #                parent is:  [ 2, -3, 3, -2, 4, -4, 5, -5]
    #     b = a.substring(a_str, 1, 5)  # #[-3, 3, -2, 4]
    #     self.assertEqual(b[0], -3)
    #     self.assertEqual(b[1], 3)
    #     self.assertEqual(b[-1], 4)

    #     c = a.substring(a_str1, 8)  # [-3, 3, -2, 4, -4, 5, -5]
    #     c_str = c.get_pos()
    #     self.assertEqual(c[0], -3)
    #     self.assertEqual(c[1], 3)
    #     self.assertEqual(c[-1], -5)

    #     d = c.substring(c_str, 1, 5)  # [3, -2, 4, -4]
    #     self.assertEqual(d[0], 3)
    #     self.assertEqual(d[1], -2)
    #     self.assertEqual(d[-1], -4)

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
        a = create_tree()
        expected = [2, -3, 3, -2, 4, -4, 5, -5]
        self.assertEqual(a.difference_sequence(a.E(),
                                               (0, 0),
                                               a.heavy_path()),
                         expected)

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

        c = create_tree_c()
        expected = [2, 5, 6, 9]
        result = c.special_subtrees()
        result.sort()
        result = map(lambda x: x.label, result)
        self.assertEqual(result, expected)

    def test_multiple_difference_sequences(self):
        c = create_tree_c()
        c.special_subtrees()

    def test_string_removal(self):
        # a = Euler_String("abcd", "adcb")
        # b = Euler_String("a", "a")
        # self.assertEqual(a.remove('a').string, "bcd")
        # self.assertEqual(a.remove('d').string, "abc")
        # self.assertEqual(a.remove('a').remove('d').string, "bc")
        # self.assertTrue(b.remove('a').is_empty())
        # self.assertRaises(Exception, a.remove, 'c')

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
        # a = Euler_String("", "")
        # b = Euler_String("a", "a")
        # c = b.remove("a")

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

    def test_match(self):
        k = Klein()
        a = Euler_String([1, 2, 3, 4])
        a_pos = a.get_pos()
        b = Euler_String([])
        b_pos = b.get_pos()
        c = Euler_String([])
        c_pos = c.get_pos()

        self.assertEqual(k.match(b, b_pos, c, c_pos), 0)
        self.assertEqual(k.match(a, a_pos, b, b_pos),
                         k.match(a, a_pos, c, c_pos))

    def test_remove_from_s(self):
        k = Klein()
        # a = Euler_String("a", "a")
        # b = Euler_String("Aa", "Aa")
        # c = Euler_String("Aa", "aA")
        # e = Euler_String("abcdDCBA", "AaBbCcDd")
        # f = Euler_String("abcdDC", "abcdDC")
        # empty = Euler_String(0, 0)

        a = Euler_String([1])
        a_pos = a.get_pos()
        b = Euler_String([-1, 1])
        b_pos = b.get_pos()
        c = Euler_String([-1, 1])
        c_pos = c.get_pos()
        e = Euler_String([1, 2, 3, 4, -4, -3, -2, -1])
        e_pos = e.get_pos()
        f = Euler_String([1, 2, 3, 4, -4, -3])
        f_pos = f.get_pos()
        empty = Euler_String([])
        empt_pos = empty.get_pos()

        self.assertEqual(k.delete_from_s(empty, e_pos, empty, e_pos),
                         float('inf'))
        self.assertEqual(k.delete_from_s(a, a_pos, empty, empt_pos), 0)
        self.assertEqual(k.delete_from_s(b, b_pos, empty, empt_pos), 1)
        self.assertEqual(k.delete_from_s(c, c_pos, empty, empt_pos), 1)
        self.assertEqual(k.delete_from_s(e, e_pos, empty, empt_pos), 4)
        self.assertEqual(k.delete_from_s(f, f_pos, empty, empt_pos), 2)
        self.assertEqual(k.delete_from_s(e, e_pos, f, f_pos), 2)

    def test_remove_from_t(self):
        k = Klein()

        a = create_tree().E()
        b = create_tree_b().E()
        bp = create_tree_b().E()
        c = create_tree_c().E()
        one = create_tree_singleton().E()

        self.assertEqual(k.delete_from_t(one, one), float('inf'))
        self.assertEqual(k.delete_from_t(one, a), 5)
        self.assertEqual(k.delete_from_t(one, b), 11)
        self.assertEqual(k.delete_from_t(one, bp), 11)
        self.assertEqual(k.delete_from_t(one, c), 11)
        pass

    def test_has_mate(self):
        # a = Euler_String("aAbBCcDf", "")

        # self.assertTrue(a.has_mate("a"))
        # self.assertTrue(a.has_mate("A"))
        # self.assertTrue(a.has_mate("c"))
        # self.assertTrue(a.has_mate("d"))
        # self.assertFalse(a.has_mate("D"))
        # self.assertFalse(a.has_mate("f"))
        # self.assertFalse(a.has_mate("g"))

        a = Euler_String([1, -1, 2, -2, -3, 3, -4, 5])

        self.assertTrue(a.has_mate(1))
        self.assertTrue(a.has_mate(-1))
        self.assertTrue(a.has_mate(3))
        self.assertTrue(a.has_mate(4))
        self.assertFalse(a.has_mate(-4))
        self.assertFalse(a.has_mate(5))
        self.assertFalse(a.has_mate(6))


#   a
#  / \
# b   c
# |
# d
# |
# e

if(__name__ == '__main__'):
    unittest.main()
