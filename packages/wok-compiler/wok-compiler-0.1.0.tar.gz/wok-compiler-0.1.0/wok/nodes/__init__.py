from .node import Node
from .table_node import TableNode
from .meta_node import MetaNode
from .heading_node import HeadingNode
from .root_node import RootNode


def cls_for_node_name(name):
    if name == "table":
        return TableNode
    elif name == "meta":
        return MetaNode
    elif name.lstrip("h") == "" and 1 <= len(name) <= 4:
        return HeadingNode
    elif name == "":
        return RootNode

    return Node
