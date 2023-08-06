#!/usr/bin/env python3
from wok.parser import Parser
from wok.formatters import formatters
import argparse
import os
from pathlib import Path


def run():
    argparser = argparse.ArgumentParser(
        description="CLI tool to parse and transform Wok files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argparser.add_argument("files", type=str, nargs="+", help="the files to compile")
    argparser.add_argument(
        "-d",
        "--dest",
        type=str,
        help="where to write the compiled files to",
        default="dist/",
    )
    argparser.add_argument(
        "-t",
        "--to",
        type=str,
        help="which type of content to compile to",
        choices=formatters.keys(),
        default="html",
    )

    args = argparser.parse_args()

    base = Path(os.path.commonpath(args.files))
    if base.is_file():
        base = base.parent
    base = str(base)
    parser = Parser()

    for file in args.files:
        target = os.path.splitext(file)[0] + "." + formatters[args.to].dest_ext
        if base != ".":
            target = target[len(base) + 1 :]
        target = os.path.join(args.dest, target)

        tree = parser.parse_file(str(Path(file).absolute()), project_dir=base)
        output = formatters[args.to].format(tree)

        Path(target).parent.mkdir(parents=True, exist_ok=True)

        with open(target, "w") as f:
            f.write(output)

        print("Compiled " + str(Path(file).absolute()) + "  --->   " + target)


if __name__ == "__main__":
    run()
