from .formatter import Formatter
import markdown


def _fmt_t(f, node):
    return node.value


def _fmt_md(f, node):
    return markdown.markdown(node.value)


def _fmt_html(f, node):
    # TODO: Strip HTML?
    return node.value


txt_formatter = Formatter()
txt_formatter.dest_ext = "txt"
txt_formatter.add_impl("t", _fmt_t)
txt_formatter.add_impl("md", _fmt_md)
txt_formatter.add_impl("html", _fmt_html)
