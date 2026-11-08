"""Command line entry point for wc-cli.

The CLI is deliberately thin: it parses arguments, delegates the counting
to :mod:`wc_cli.counter`, writes the table to stdout and the per-file
errors to stderr.  No counting logic lives here.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from wc_cli.counter import FileReadError, FileStats, count_file, render_table


def main(argv: Sequence[str] | None = None) -> int:
    """Count the given files and print the statistics table.

    A table is printed even when some files fail: the failed ones are
    reported on stderr and skipped in the table.

    :param argv: command line arguments; ``None`` means ``sys.argv[1:]``.
    :return: 0 on success, 1 if at least one file could not be read.
    :raises SystemExit: exit code 2 on invalid arguments (usage error).
    """
    args = _build_parser().parse_args(argv)
    stats: list[FileStats] = []
    had_read_error = False
    for file_arg in args.files:
        try:
            stats.append(count_file(Path(file_arg)))
        except FileReadError as error:
            print(f"wc: {error}", file=sys.stderr)
            had_read_error = True
    print(render_table(stats))
    return 1 if had_read_error else 0


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for wc-cli.

    :return: a parser with a required positional ``files`` (one or more paths).
    """
    parser = argparse.ArgumentParser(
        prog="wc-cli",
        description="Count lines, words and characters in text files.",
    )
    parser.add_argument("files", nargs="+", metavar="FILE", help="files to count")
    return parser
