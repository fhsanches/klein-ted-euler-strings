#!/usr/bin/env python3

from klein import Klein_TED
# from state import getstate
from sys import argv

import random


# from guppy import hpy #profiler
# import timeit
from timeit import default_timer as timer

import numpy as np
import sys

# sys.setrecursionlimit(100000)  # Python is a good language.


def create_random_balanced_tree(size=10):
    tree = {0: []}

    for node_num in range(1, size):
        parent_candidates = []
        weigth = []

        for pc in range(0, node_num):
            if pc not in tree:
                tree[pc] = []

            # w = (1 - node_num - len(tree[pc]))/(node_num)
            w = 1/(len(tree[pc])+1)
            parent_candidates.append(pc)
            weigth.append(w)

        # print("pc = " + str(parent_candidates))
        # print("we = " + str(weigth))

        parent = random.choices(parent_candidates, weigth)[0]

        tree[parent].append(node_num)

    # print(tree)

    return tree


def create_random_unbalanced_tree(size=10):
    tree = {0: []}
    nodes = [0]

    for node_num in range(1, size):

        parent = random.choices(nodes)[0]

        if parent not in tree:
            tree[parent] = []

        tree[parent].append(node_num)
        nodes.append(node_num)

    return tree


# def create_random_unbalanced_tree(size=10):
#     tree = {0 : []}

#     for node_num in range(1,size): # for every node to be created minus the root
#         parent = random.randrange(0, node_num)

#         if parent not in tree:
#             tree[parent] = []

#         tree[parent].append(node_num)


#     for node_num in range(2,size): # adding leaves
#         if node_num not in tree:
#             tree[node_num] = []

#     return tree


def change_tree_randomly(tree, num_changes=10, seed=100):
    # find a pair of siblings
    # TODO

    # randomly iterate to some of its descendants
    # TODO

    # swap the children of the chosen desdendants
    # TODO
    pass


def test_for_size(size_F=10, size_G=10, trials=10, is_imba=False):
    timers = []
    calls = []
    distances = []

    for x in range(0, trials):
        if(is_imba):
            t1 = create_random_unbalanced_tree(size_F)
            t2 = create_random_unbalanced_tree(size_G)
        else:
            t1 = create_random_balanced_tree(size_F)
            t2 = create_random_balanced_tree(size_G)

        start = timer()
        (dist, ncalls) = Klein_TED(t1, t2)
        end = timer()

        time = end-start

        # res = (dist, ncalls, time)
        timers.append(time)
        calls.append(ncalls)
        distances.append(dist)

        # res = (dist, ncalls, time)
        # results.append(res)

    times = np.array(timers)
    t_mean = np.mean(times)
    t_std = np.std(times)

    calls = np.array(calls)
    c_mean = np.mean(calls)
    c_std = np.std(calls)

    print(str(size_F) + ',' +
          str(size_G) + ',' +
          str(t_mean) + ',' +
          str(t_std) + ',' +
          str(c_mean) + ',' +
          str(c_std))

    # print("|F|,|G|, dist, #calls, time")
    # for (dist, calls, time) in results:
    #     print(str(size_F) + "," +
    #           str(size_G) + "," +
    #           str(dist) + "," +
    #           str(calls) + "," +
    #           str(time))


def test(seed=0):

    # USE_STATE = False

    # if(USE_STATE):
    #     random.setstate(random.getstate())
    # else:
    #     random.seed(seed)

    if(len(argv) < 4):
        print("Usage: ./random_test.py |F| |G| #trials")
        return

    # print(argv)
    (size_F, size_G, trials) = map(lambda x: int(x), argv[1:4])

    random.seed(seed)

    # for size in [40, 50, 60, 70, 80, 90,100,110,120,130]:
    #     size_F = size
    #     size_G = size + 10
    #     test_for_size(size_F, size_G, trials, True)

    # for size in [40, 50, 60, 70, 80, 90]:
    #     size_F = size
    #     size_G = 90
    #     test_for_size(size_F, size_G, trials, True)

    # for size in [40, 50, 60, 70, 80, 90]:
    #     size_F = size
    #     size_G = 90
    #     test_for_size(size_F, size_G, trials, True)



    if(len(argv) > 4):
        test_for_size(size_F, size_G, trials, True)
        return
    else:
        test_for_size(size_F, size_G, trials, False)


# h = hpy()
# print h.heap()

test()
