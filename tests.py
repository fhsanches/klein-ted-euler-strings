#!/usr/bin/env python3

from klein import Arc, Node
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
# tree.create_arcs()


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
        print("euler: " + tree.euler())
        print(tree.arcs)
        print(tree.arcs[0].label)


if __name__ == '__main__':
    unittest.main()


def run():
    unittest.main()
