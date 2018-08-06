#!/usr/bin/env python3

from klein import Node, remove
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
        self.assertEqual(a.euler(), "bdeEDBcC")
        self.assertEqual(a.children[0].euler(), "deED")
        self.assertEqual(a.children[1].euler(), "")

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

    def string_removal(self):
        a = "abcd"
        self.assertEqual(remove(a, 'a'), "bcd")
        self.assertEqual(remove(a, 'd'), "abc")
        self.assertRaises(Exception, remove, a, 'c')


#   a
#  / \
# b   c
# |
# d
# |
# e

if(__name__ == '__main__'):
    unittest.main()
