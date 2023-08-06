from . import Node


class RootNode(Node):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.file_path = ""
