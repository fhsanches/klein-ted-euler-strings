#!/usr/bin/env python3

from klein import Node, Euler_String, Euler_Substring, Klein, list_split
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

    a.post_processing()

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
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)
    f = Node(6)
    g = Node(7)
    h = Node(8)
    i = Node(9)
    j = Node(10)
    k = Node(11)
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

    a.post_processing()

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
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)
    f = Node(6)
    g = Node(7)
    h = Node(8)
    i = Node(9)
    j = Node(10)
    k = Node(11)

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

    return a


tree = create_tree()


class TestSuite(unittest.TestCase):

    k = Klein()

    def test_list_split(self):
        ls = [1, 2, 3, 4]
        self.assertEqual(list_split(ls, 3), [[1, 2], [4]])
        self.assertEqual(list_split(ls, 2), [[1], [3, 4]])

    def test_arc(self):
        if(len(tree.arcs) == 0):
            return

        a = tree.arcs[0]

        self.assertEqual(a.mate.mate, a)
        self.assertEqual(a.s, a.mate.t)
        self.assertEqual(a.t, a.mate.s)
        self.assertEqual(a.mate, a.mate.mate.mate)

    def test_euler(self):
        a = create_tree()
        # self.assertEqual(a.E(), "bdeEDBcC")
        self.assertEqual(a.E(), [2, 4, 5, -5, -4, -2, 3, -3])
        # self.assertEqual(a.children[0].E(), "deED")
        self.assertEqual(a.children[0].E(), [4, 5, -5, -4])
        self.assertEqual(a.children[1].E(), [])

    def test_string_index(self):
        a = Euler_String([2, -3, 3, -2, 4, -4, 5, -5])
        self.assertEqual(a[0], 2)
        self.assertEqual(a[1], -3)
        self.assertEqual(a[-1], -5)

        #                            [ 0,  1, 2,  3, 4,  5, 6,  7]
        #                            [-8, -7,-6, -5,-4, -3,-2, -1]
        #                parent is:  [ 2, -3, 3, -2, 4, -4, 5, -5]
        b = a.substring(1, 5)  # #[-3, 3, -2, 4]
        self.assertEqual(b[0], -3)
        self.assertEqual(b[1], 3)
        self.assertEqual(b[-1], 4)

        c = a.substring(1, 8)  # [-3, 3, -2, 4, -4, 5, -5]
        self.assertEqual(c[0], -3)
        self.assertEqual(c[1], 3)
        self.assertEqual(c[-1], -5)

        d = c.substring(1, 5)  # [3, -2, 4, -4]
        self.assertEqual(d[0], 3)
        self.assertEqual(d[1], -2)
        self.assertEqual(d[-1], -4)

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
        # expected = "bCcBdDeE"
        expected = [2, -3, 3, -2, 4, -4, 5, -5]
        self.assertEqual(a.difference_sequence(a.heavy_path()), expected)

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

    def test_string_removal(self):
        # a = Euler_String("abcd", "adcb")
        # b = Euler_String("a", "a")
        # self.assertEqual(a.remove('a').string, "bcd")
        # self.assertEqual(a.remove('d').string, "abc")
        # self.assertEqual(a.remove('a').remove('d').string, "bc")
        # self.assertTrue(b.remove('a').is_empty())
        # self.assertRaises(Exception, a.remove, 'c')

        a = Euler_String([1, 2, 3, 4])
        b = Euler_String([1])
        self.assertEqual(a.remove(1).string, [2, 3, 4])
        self.assertEqual(a.remove(4).string, [1, 2, 3])
        self.assertEqual(a.remove(1).remove(4).string, [2, 3])
        self.assertTrue(b.remove(1).is_empty())
        self.assertRaises(Exception, a.remove, 3)

    def test_is_empty(self):
        # a = Euler_String("", "")
        # b = Euler_String("a", "a")
        # c = b.remove("a")

        a = Euler_String([])
        b = Euler_String([1])
        c = b.remove(1)

        self.assertTrue(a.is_empty())
        self.assertFalse(b.is_empty())
        self.assertTrue(c.is_empty())

    def test_split_first(self):
        # a = Euler_String("bcdaDCBA", "bABcCDda")

        # expected_e = ("b", "B")
        # expected_res_str = ("cdaDC", "A")
        # expected_res_diff = ("cCDda", "A")

        # (e, res1, em, res2) = a.split_first("b", True)

        a = Euler_String([2, 3, 4, 1, -4, -3, -2, -1])

        expected_e = (2, -2)
        expected_tp_tpp_str = ([3, 4, 1, -4, -3], [-1])

        (e, tpp, em, tp) = a.split_first(2, True)

        self.assertEqual((e, em), expected_e)
        self.assertEqual((tpp.string, tp.string), expected_tp_tpp_str)

    def test_split_last(self):
        # a = Euler_String("bcdaDCBA", "AbBcCDda")

        # expected_e = ("A", "a")
        # expected_res_str = ("bcd", "DCB")
        # expected_res_diff = ("", "bBcCDd")

        # (res1, em, res2, e) = a.split_last("A", True)

        a = Euler_String([2, 3, 4, 1, -4, -3, -2, -1])

        expected_e = (-1, 1)
        expected_res_str = ([2, 3, 4], [-4, -3, -2])

        (res1, em, res2, e) = a.split_last(-1, True)

        self.assertEqual((e, em), expected_e)
        self.assertEqual((res1.string, res2.string), expected_res_str)

    def test_match(self):
        k = Klein()
        a = Euler_String([1, 2, 3, 4])
        b = Euler_String([])
        c = Euler_String([])
        self.assertEqual(k.match(b, c), 0)
        self.assertEqual(k.match(a, b), k.match(a, c))

    def test_remove_from_s(self):
        k = Klein()
        # a = Euler_String("a", "a")
        # b = Euler_String("Aa", "Aa")
        # c = Euler_String("Aa", "aA")
        # e = Euler_String("abcdDCBA", "AaBbCcDd")
        # f = Euler_String("abcdDC", "abcdDC")
        # empty = Euler_String(0, 0)

        a = Euler_String([1])
        b = Euler_String([-1, 1])
        c = Euler_String([-1, 1])
        e = Euler_String([1, 2, 3, 4, -4, -3, -2, -1])
        f = Euler_String([1, 2, 3, 4, -4, -3])
        empty = Euler_String([])

        self.assertEqual(k.delete_from_s(empty, empty), float('inf'))
        self.assertEqual(k.delete_from_s(a, empty), 0)
        self.assertEqual(k.delete_from_s(b, empty), 1)
        self.assertEqual(k.delete_from_s(c, empty), 1)
        self.assertEqual(k.delete_from_s(e, empty), 4)
        self.assertEqual(k.delete_from_s(f, empty), 2)
        self.assertEqual(k.delete_from_s(e, f), 2)
        pass

    def test_remove_from_t(self):
        k = Klein()
        # a = Euler_String("a", "a")
        # b = Euler_String("Aa", "Aa")
        # c = Euler_String("Aa", "aA")
        # e = Euler_String("abcdDCBA", "AaBbCcdD")
        # f = Euler_String("abcdDC", "abcdDC")
        # empty = Euler_String("", "")

        a = Euler_String([1])
        b = Euler_String([-1, 1])
        c = Euler_String([-1, 1])
        e = Euler_String([1, 2, 3, 4, -4, -3, -2, -1])
        f = Euler_String([1, 2, 3, 4, -4, -3])
        empty = Euler_String([])

        self.assertEqual(k.delete_from_t(empty, empty), float('inf'))
        self.assertEqual(k.delete_from_t(empty, a), 0)
        self.assertEqual(k.delete_from_t(empty, b), 1)
        self.assertEqual(k.delete_from_t(empty, c), 1)
        self.assertEqual(k.delete_from_t(empty, e), 4)
        self.assertEqual(k.delete_from_t(empty, f), 2)
        self.assertEqual(k.delete_from_t(f, e), 2)
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
