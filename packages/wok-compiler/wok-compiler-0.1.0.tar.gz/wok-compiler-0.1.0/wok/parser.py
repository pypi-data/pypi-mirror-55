from wok.nodes import Node, cls_for_node_name, RootNode
from pathlib import Path
from glob import glob


class Parser:
    def __init__(self):
        """
        Caches the node tree of previously parsed files
        """
        self.file_cache = {}

    def parse_file(self, file_path, project_dir=".", recursive=3):
        """
        Parses a file and returns the node tree

        Params:
            - file_path: Absolute path to the file to analyse
            - recursive: Whether to follow source="" links or not
        """
        context = {"line": 0, "indent": 0, "file_path": file_path}

        f = open(file_path, "r")
        tree = self.parse_str(f.read(), context)
        tree.file_path = file_path
        f.close()

        if recursive > 0:
            for node in tree.flatten():
                if isinstance(node, Node) and "source" in node.params:
                    if node.params["source"].startswith("/"):
                        fpath = Path(project_dir) / node.params["source"].lstrip("/")
                    else:
                        fpath = Path(file_path).parent / node.params["source"]

                    files = glob(str(fpath.absolute()))

                    for fpath in files:
                        node.linked_to.append(
                            self.parse_file(fpath, project_dir=project_dir, recursive=recursive - 1)
                        )

        return tree

    def parse_str(self, wok_str, context):
        lines = list(enumerate(wok_str.split("\n")))
        levels = [RootNode()]

        while len(lines) > 0:
            line_n, line = lines.pop(0)
            sline = line.strip()

            if sline == "" or sline.startswith("//"):
                continue

            if sline.startswith("_"):
                raise Exception("Illegal name starts with _")
                continue

            if sline.startswith("| "):
                line = line.replace("| ", "_textnode ", 1)
            elif sline.startswith("|"):
                line = line.replace("|", "_textnode ", 1)

            indent = self._indentof(line) // 4
            # TODO: validate indent
            node = self._parse_node(
                line,
                lines,
                {**context, "line": line_n + context["line"], "indent": indent},
            )

            levels = levels[: int(indent) + 1]

            node.parent = levels[int(indent)]
            levels[int(indent)].children.append(node)
            levels.append(node)

        return levels[0]

    def _parse_node(self, line, lines, context, is_inline=False):
        """
        Parses a single node.

        Params:
            - line: The line to parse (array of chars)
            - lines: Array of lines left to parse, not containing line
            - context: The parsing context
        """
        if type(line) != list:
            chars = list(line.strip().lstrip("+"))
        else:
            chars = line

        name = self._read_word(chars)
        node = cls_for_node_name(name)()
        node.name = name

        self._parse_node_params(chars, node)
        self._parse_node_value(chars, lines, node, context, is_inline=is_inline)

        return node

    def _parse_node_params(self, chars, node):
        if len(chars) == 0 or chars[0] != "(":
            return

        chars.pop(0)
        word = self._read_word(chars)

        while len(word) > 0:
            if chars[0] == "=":
                chars.pop(0)
                node.params[word] = self._read_value(chars)
            else:
                node.params[word] = "yes"

            word = self._read_word(chars)

        assert chars[0] == ")", "Incorrectly ended parameters"
        chars.pop(0)

    def _parse_node_value(self, chars, lines, node, context, is_inline=False):
        if len(chars) == 0:
            return

        if chars[0] == "." and len(lines) > 0 and not is_inline:
            # Multi-line value
            line_n, line = lines[0]
            indent = self._indentof(line)

            while len(lines) > 0 and indent >= 4 * (context["indent"] + 1):
                extra_indent = indent - 4 * (context["indent"] + 1)
                node.children += [
                    (" " * extra_indent),
                    *(self._parse_node_value_string(list(line.lstrip()))),
                    "\n",
                ]

                lines.pop(0)
                if len(lines) > 0:
                    line_n, line = lines[0]
                    indent = self._indentof(line)
        else:
            if chars[0] == " ":
                chars.pop(0)

            # Single-line value
            node.children += self._parse_node_value_string(chars, is_inline=is_inline)

    def _parse_node_value_string(self, chars, is_inline=False):
        children = [""]
        escaping = False
        constructing = False

        while len(chars) > 0 and not (is_inline and not escaping and chars[0] == "]"):
            curr_escaping = escaping
            escaping = False

            if (
                not curr_escaping
                and len(chars) >= 4
                and chars[0] == "#"
                and chars[1] == "["
            ):
                chars.pop(0)
                chars.pop(0)
                children.append(self._parse_node(chars, [], {}, is_inline=True))
                children.append("")
                chars.pop(0)
                continue

            if chars[0] == "\\" and not curr_escaping:
                chars.pop(0)
                escaping = True
            else:
                children[len(children) - 1] += chars.pop(0)

        return filter(lambda child: type(child) != str or len(child) > 0, children)

    def _read_word(self, chars):
        word = ""

        while len(chars) > 0 and (
            (chars[0].isalpha() or chars[0] == "_")
            or (len(word) == 0 and chars[0] == " ")
        ):
            char = chars.pop(0)
            if char.isalpha() or char == "_":
                word += char

        return word

    def _read_value(self, chars):
        if len(chars) == 0:
            return ""

        if chars[0] != '"':
            return _read_word(chars)

        chars.pop(0)
        escaping = False
        value = ""

        while len(chars) > 0 and (chars[0] != '"' or escaping):
            escaping = False

            if chars[0] == "\\":
                escaping = True
            else:
                value += chars.pop(0)

        assert chars[0] == '"', "Unended string in parameters"
        chars.pop(0)

        return value

    def _indentof(self, s):
        if type(s) is list or type(s) is tuple:
            s = "".join(s)

        return len(s) - len(s.lstrip(" "))
