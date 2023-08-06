class Formatter:
    def __init__(self):
        self.blocks_impl = {
            "": lambda f, node: "\n".join([f(child) for child in node.children]),
            "meta": lambda f, node: "",
            "_textnode": lambda f, node: "".join(f(node.children)),
        }
        self.dest_ext = ""

    def add_impl(self, block, f):
        self.blocks_impl[block] = f

    def format(self, node):
        if type(node) is str:
            return node

        if type(node) is list:
            # The map is there to prevent double-escapes from happening (for example in HTML)
            return "".join(
                map(
                    lambda child: self.format(child) if type(child) != str else child,
                    node,
                )
            )

        if node.get_block_name() in self.blocks_impl:
            return self.blocks_impl[node.get_block_name()](self.format, node)

        print(f"WARN: Undefined block {node.name}")
        return ""
