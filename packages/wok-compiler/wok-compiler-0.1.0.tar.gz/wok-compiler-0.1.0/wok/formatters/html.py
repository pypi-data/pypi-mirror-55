from .formatter import Formatter
import markdown
import html
from os.path import relpath


class HTMLFormatter(Formatter):
    def format(self, node):
        if type(node) == str:
            return html.escape(node)

        return super().format(node)


def _fmt_t(f, node):
    return f"<p>{f(node.children)}</p>"


def _fmt_md(f, node):
    return markdown.markdown(f(node.children))


def _fmt_html(f, node):
    return f(node.children)


def _fmt_raw(f, node):
    return f"<pre>{f(node.children)}</pre>"


def _fmt_row(f, node):
    html = '<div class="row">'

    for column in node.select_all("column"):
        html += f'<div class="column">{f(column.children)}</div>'

    html += "</div>"
    return html


def _fmt_h(f, node):
    level = len(node.name)

    return f"<h{level}>{f(node.children)}</h{level}>"


def _fmt_table(f, node):
    return ""


def _fmt_link(f, node):
    # TODO: maybe some smart parsing of the link?
    return f'<a href="{ node.params.get("to") }">{f(node.children)}</a>'


def _fmt_embed(f, node):
    curr_path = node.root().file_path
    embeds = []

    node.linked_to = sorted(
        node.linked_to,
        key=lambda n: int(
            n.select("meta").get_value(node.params.get("orderby", "order"), 1)
        ),
        reverse=node.params.get("reverse", "no") == "yes",
    )

    for linked_node in node.linked_to:
        link = relpath(linked_node.file_path, curr_path)
        embeds.append(
            '<a class="embed" href="{}"><span class="embed-emoji">{}</span><span><span class="embed-title">{}</span></span></a>'.format(
                link[:-4] if link.endswith(".wok") else link,
                linked_node.select("meta").get_value("emoji", "📄"),
                linked_node.select("meta").get_value("title"),
            )
        )

    return "\n".join(embeds)


def _fmt_callout(f, node):
    return '<div class="callout"><div class="callout-emoji">{}</div><div class="callout-title">{}</div></div>'.format(
        node.params.get("emoji", "💡"), f(node.children),
    )


def _fmt_quote(f, node):
    return "<blockquote>{}</blockquote>".format(f(node.children))


html_formatter = HTMLFormatter()
html_formatter.dest_ext = "html"
html_formatter.add_impl("t", _fmt_t)
html_formatter.add_impl("h", _fmt_h)
html_formatter.add_impl("md", _fmt_md)
html_formatter.add_impl("html", _fmt_html)
html_formatter.add_impl("raw", _fmt_raw)
html_formatter.add_impl("row", _fmt_row)
html_formatter.add_impl("table", _fmt_table)
html_formatter.add_impl("link", _fmt_link)
html_formatter.add_impl("embed", _fmt_embed)
html_formatter.add_impl("quote", _fmt_quote)
html_formatter.add_impl("callout", _fmt_callout)
