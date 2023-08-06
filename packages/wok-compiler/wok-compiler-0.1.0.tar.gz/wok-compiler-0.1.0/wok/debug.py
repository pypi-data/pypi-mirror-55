from wok.nodes import Node


def print_tree(tree, lvl=0):
    print(("    " * lvl) + repr(tree))

    if isinstance(tree, Node):
        for child in tree.children:
            print_tree(child, lvl + 1)
