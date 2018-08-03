#!/usr/bin/env python3

from klein import Node
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
        self.assertEqual(a.euler(), "bdee'd'b'cc'")
        self.assertEqual(a.children[0].euler(), "dee'd'")
        self.assertEqual(a.children[1].euler(), "")


if __name__ == '__main__':
    unittest.main()
