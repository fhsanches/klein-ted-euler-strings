#!/usr/bin/env python3

from klein import *
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


class TestSuite(unittest.TestCase):
    def test_arc(self):
        a = Arc(1,2)

        self.assertEqual(a.mate.mate, a)
        self.assertEqual(a.s, a.mate.t)
        self.assertEqual(a.t, a.mate.s)

    def test_tree(self):
        print "TESTING TREE"
        a = create_tree()
        a.create_arcs()
        print a.euler()



        

if __name__ == '__main__':
    unittest.main()

def run():
    unittest.main()
