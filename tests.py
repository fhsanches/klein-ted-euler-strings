#!/usr/bin/env python3

from klein import Node, Euler_String, Klein
import unittest


def create_tree():
    a = Node('a')
    b = Node('b')
    c = Node('c')
    d = Node('d')
    e = Node('e')

    a.add_child(b)
    a.add_child(c)
    b.add_child(d)
    d.add_child(e)

    a.post_processing()

    return a

#   a
#  / \
# b   c
# |
# d
# |
# e


tree = create_tree()


class TestSuite(unittest.TestCase):

    k = Klein()

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
        self.assertEqual(a.E(), "bdeEDBcC")
        self.assertEqual(a.children[0].E(), "deED")
        self.assertEqual(a.children[1].E(), "")

    def test_weights(self):
        a = create_tree()
        self.assertEqual(a.weigth, 5)
        self.assertEqual(a.children[0].weigth, 3)
        self.assertEqual(a.children[1].weigth, 1)

    def test_heavy_path(self):
        a = create_tree()
        expected = ["a", "b", "d", "e"]
        output_ls = a.heavy_path()
        output = map(lambda x: x.label, output_ls)
        self.assertEqual(output, expected)

    def test_difference_sequence(self):
        a = create_tree()
        expected = "bCcBdDeE"
        self.assertEqual(a.difference_sequence(a.heavy_path()), expected)

    def test_string_removal(self):
        a = Euler_String("abcd", "adcb")
        b = Euler_String("a", "a")
        self.assertEqual(a.remove('a').string, "bcd")
        self.assertEqual(a.remove('d').string, "abc")
        self.assertEqual(a.remove('a').remove('d').string, "bc")
        self.assertTrue(b.remove('a').is_empty())
        self.assertRaises(Exception, a.remove, 'c')

    def test_is_empty(self):
        a = Euler_String("", "")
        b = Euler_String("a", "a")
        c = b.remove("a")
        self.assertTrue(a.is_empty())
        self.assertFalse(b.is_empty())
        self.assertTrue(c.is_empty())

    def test_split_first(self):
        a = Euler_String("bcdaDCBA", "bABcCDda")

        expected_e = ("b", "B")
        expected_res_str = ("cdaDC", "A")
        expected_res_diff = ("cCDda", "A")

        (e, res1, em, res2) = a.split_first("b", True)

        self.assertEqual((e, em), expected_e)
        self.assertEqual((res1.string, res2.string), expected_res_str)
        self.assertEqual((res1.diff, res2.diff), expected_res_diff)

    def test_split_last(self):
        a = Euler_String("bcdaDCBA", "AbBcCDda")

        expected_e = ("A", "a")
        expected_res_str = ("bcd", "DCB")
        expected_res_diff = ("", "bBcCDd")

        (res1, em, res2, e) = a.split_last("A", True)

        self.assertEqual((e, em), expected_e)
        self.assertEqual((res1.string, res2.string), expected_res_str)
        self.assertEqual((res1.diff, res2.diff), expected_res_diff)

    def test_match(self):
        k = Klein()
        a = Euler_String("abcd", "adcb")
        b = Euler_String("", "")
        c = Euler_String("", "")
        self.assertEqual(k.match(b, c), 0)
        self.assertEqual(k.match(a, b), k.match(a, c))

    def test_remove_from_s(self):
        k = Klein()
        a = Euler_String("a", "a")
        b = Euler_String("Aa", "Aa")
        c = Euler_String("Aa", "aA")
        e = Euler_String("abcdDCBA", "AaBbCcDd")
        f = Euler_String("abcdDC", "abcdDC")
        empty = Euler_String("", "")
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
        a = Euler_String("a", "a")
        b = Euler_String("Aa", "Aa")
        c = Euler_String("Aa", "aA")
        e = Euler_String("abcdDCBA", "AaBbCcdD")
        f = Euler_String("abcdDC", "abcdDC")
        empty = Euler_String("", "")
        self.assertEqual(k.delete_from_t(empty, empty), float('inf'))
        self.assertEqual(k.delete_from_t(empty, a), 0)
        self.assertEqual(k.delete_from_t(empty, b), 1)
        self.assertEqual(k.delete_from_t(empty, c), 1)
        self.assertEqual(k.delete_from_t(empty, e), 4)
        self.assertEqual(k.delete_from_t(empty, f), 2)
        self.assertEqual(k.delete_from_t(f, e), 2)
        pass

    def test_has_mate(self):
        a = Euler_String("aAbBCcDf", "")

        self.assertTrue(a.has_mate("a"))
        self.assertTrue(a.has_mate("A"))
        self.assertTrue(a.has_mate("c"))
        self.assertTrue(a.has_mate("d"))
        self.assertFalse(a.has_mate("D"))
        self.assertFalse(a.has_mate("f"))
        self.assertFalse(a.has_mate("g"))



#   a
#  / \
# b   c
# |
# d
# |
# e

if(__name__ == '__main__'):
    unittest.main()
