flatten = lambda l: [item for sublist in l for item in sublist]


class Node:
    def __init__(self, parent=None):
        self.name = ""
        self.params = {}

        """
        Array of Node|str
        """
        self.children = []

        """
        Array of Node (root nodes of other documents)
        """
        self.linked_to = []

        """
        Parent Node of this Node
        """
        self.parent = parent

    def get_block_name(self):
        return self.name

    def __repr__(self):
        params = " ".join([f'{k}="{v}"' for (k, v) in self.params.items()])
        if len(params):
            params = f"({params})"

        value = self.value().split("\n")[0]
        if len(value) > 64:
            value = value[:61]
            value += "..."
        if len(value):
            value = " " + value

        return f"Node<{self.name}{params}{value}>"

    def __str__(self):
        params = " ".join([f'{k}="{v}"' for (k, v) in self.params.items()])
        if len(params):
            params = f"({params})"

        value = self.value()
        if "\n" in value:
            value = ".\n" + "\n".join(["    " + line for line in value.splitlines()])
        else:
            value = " " + value

        return f"{self.name}{params}{value}"

    def root(self):
        ref = self

        while ref.name != "" and ref.parent:
            ref = ref.parent

        return ref if ref.name == "" else None

    def flatten(self):
        arr = [self]
        for child in self.children:
            arr.extend(child.flatten() if isinstance(child, Node) else [child])
        return arr

    def value(self):
        if len(self.children) != 1 or (
            type(self.children[0]) != str and self.children[0].name != "_textblock"
        ):
            return ""

        if type(self.children[0]) == str:
            return self.children[0]
        else:
            return self.children[0].value()

    def select(self, q):
        for child in self.children:
            if child.name == q:
                return child

    def select_all(self, q):
        return [child for child in self.children if child.name == q]
