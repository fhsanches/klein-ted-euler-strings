from klein import Node, build_tree_from_dict


def create_tree():

    #   a
    #  / \
    # b   c
    # | \  \
    # d  e  g
    # |
    # f

    nodes = {
        1: [2, 3],
        2: [4, 5],
        4: [6],
        3: [7]
    }

    a = build_tree_from_dict(nodes)

    return a

def create_tree_b():

    #   a
    #  / \
    # b   c
    # | \  \
    # d  e  g
    # |
    # f

    nodes = {
        1: [2],
    }

    a = build_tree_from_dict(nodes)

    return a

t = create_tree_b()
print(t.difference_sequence(t.E()))
