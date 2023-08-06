from . import Node


class HeadingNode(Node):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def get_block_name(self):
        return "h"
