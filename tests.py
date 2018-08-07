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
        self.assertEqual(a.remove('a'), "bcd")
        self.assertEqual(a.remove('d'), "abc")
        self.assertRaises(Exception, a.remove, 'c')

    def test_match(self):
        k = Klein()
        a = Euler_String("abcd", "adcb")
        b = Euler_String("", "")
        c = Euler_String("", "")
        self.assertEqual(k.match(b, c), 0)
        self.assertEqual(k.match(a, b), k.match(a, c))

    def test_remove_from_s(self):
        k = Klein()
        a = Euler_String("abcd", "adcb")
        b = Euler_String("", "")
        self.assertEqual(k.delete_from_s(a, b), 4)
        pass


#   a
#  / \
# b   c
# |
# d
# |
# e

if(__name__ == '__main__'):
    unittest.main()
