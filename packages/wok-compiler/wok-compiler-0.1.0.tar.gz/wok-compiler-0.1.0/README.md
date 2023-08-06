# Wok

Wok is a markup language, similar to Markdown but with a syntax based on [Pug](https://pugjs.org/). I'm aiming to make Wok into some kind of middle-ground between the power of HTML and the simplicity of Markdown. The idea came from wanting an open-source alternative to [Notion](https://notion.so/), an app I find to be quite powerful.

Wok currently compiles only to HTML. A tool to compile-and-serve Wok files is available as a separate `wok-serve` package.

Example usage:

```bash
# Show help
wok -h

# Compile a few files
wok my_wok_file.wok my_other_file.wok

# Compile with glob
wok *.wok
```
