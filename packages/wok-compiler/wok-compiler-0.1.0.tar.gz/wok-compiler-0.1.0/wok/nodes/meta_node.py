from . import Node


class MetaNode(Node):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def get(self, path):
        ref = self
        path = path.split(" ")

        while ref and len(path) > 0:
            ref = ref.select(path.pop(0))

        if ref:
            return ref

    def get_value(self, path, default=None):
        ref = self.get(path)

        return ref.value() if ref else default
